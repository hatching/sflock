# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import hashlib
import io
import ntpath
import olefile
import os.path
import re
import shutil
import subprocess
import tempfile

from sflock.identify import identify
from sflock.compat import magic
from sflock.config import iter_passwords
from sflock.exception import UnpackException, MaxNestedError
from sflock.misc import data_file, make_list

MAX_NESTED = 10

class Identifier:
    name = None
    ext = []
    platform = []

    plugins = {}

    def __init__(self):
        pass

    @staticmethod
    def identify(f):
        raise NotImplementedError()

    @staticmethod
    def to_json(object):
        return {
            "name": object.name,
            "platform": object.platform
        }

class Unpacker(object):
    """Abstract class for Unpacker engines."""
    name = None
    exe = None
    exts = ()
    package = None
    magic = None
    priority = 0

    # Initiated at runtime - contains each Unpacker subclass.
    plugins = {}

    def __init__(self, f):
        self.f = f
        self.init()

    def init(self):
        pass

    def supported(self):
        return os.path.exists(self.exe)

    def zipjail(self, filepath, dirpath, *args):
        zipjail = data_file("zipjail.elf")

        p = subprocess.Popen(
            (zipjail, filepath, dirpath, "--clone=1", "--", self.exe) + args,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return_code = p.wait()
        out, err = p.communicate()

        if b"Excessive writing caused incomplete unpacking!" in err:
            self.f.error = "files_too_large"
            return False

        if b"Detected potential out-of-path arbitrary overwrite!" in err:
            self.f.error = "directory_traversal"
            return False

        if b"Blocked system call" in err and b"syscall=symlink" in err:
            self.f.error = "malicious_symlink"
            return False

        if b"Wrong password" in err:
            self.f.error = "Bad password"
            return False

        return not return_code

    def handles(self):
        if self.f.filename and self.f.filename.lower().endswith(self.exts):
            return True

        for magic in make_list(self.magic or []):
            if magic in self.f.magic:
                return True
        return False

    def decrypt(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def guess(f):
        """Guesses the unpacker based on the filename and/or contents."""
        plugins = list(Unpacker.plugins.values())
        plugins.sort(key=lambda x: x.priority, reverse=True)
        for plugin in plugins:
            if plugin(f).handles():
                yield plugin.name

    def unpack(self, depth=0, password=None, duplicates=None):
        raise NotImplementedError

    def process(self, entries, duplicates, depth, password=None):
        """Recursively unpacks embedded archives if found."""
        if duplicates is None:
            duplicates = []

        ret = []
        for f in entries:
            for unpacker in Unpacker.guess(f):
                plugin = self.plugins[unpacker](f)
                if plugin.supported():
                    depth += 1
                    if depth > MAX_NESTED:
                        raise MaxNestedError(
                            "The submitted file exceeded the maximum of %s "
                            "nested archive files" % MAX_NESTED
                        )

                    f.children = plugin.unpack(depth, password, duplicates)

                    depth -= 1

                    # TODO Improve this. The following is simply a guesstimate
                    # towards which unpacker is actually used. If there are
                    # multiple unpackers eligible for the current file, but
                    # neither unpacks anything, then f.unpacker will be set to
                    # the last available unpacker.
                    f.unpacker = unpacker
                    if f.children:
                        break

            if f.sha256 not in duplicates:
                duplicates.append(f.sha256)
            else:
                f.duplicate = True

            f.parent = self.f
            ret.append(f)
        return ret

    @staticmethod
    def single(f, password, duplicates):
        depth = 0
        return Unpacker(None).process([f], duplicates, depth, password)

    def process_directory(self, dirpath, duplicates, depth, password=None):
        """Enumerates a directory, removes the directory, and returns data
        after calling the process function."""
        entries = []
        if duplicates is None:
            duplicates = []

        if not os.listdir(dirpath):
            self.f.mode = "failed"
            self.f.error = "no files extracted"

        for dirpath2, dirnames, filepaths in os.walk(dirpath):
            for filepath in filepaths:
                filepath = os.path.join(dirpath2, filepath)
                entries.append(File(
                    relapath=filepath[len(dirpath)+1:],
                    password=password,
                    contents=open(filepath, "rb").read()
                ))

        shutil.rmtree(dirpath)
        return self.process(entries, duplicates, depth)

    def bruteforce(self, passwords, *args, **kwargs):
        if isinstance(passwords, str):
            passwords = [passwords]
        elif not passwords:
            passwords = []

        for password in iter_passwords():
            if password not in passwords:
                passwords.append(password)

        passwords.insert(0, None)
        for password in passwords:
            value = self.decrypt(password, *args, **kwargs)
            if value:
                return value

class Decoder(object):
    """Abstract class for Decoder engines."""

    # Initiated at runtime - contains each Decoder subclass.
    plugins = {}

    def __init__(self, f, password):
        self.f = f
        self.password = password
        self.init()

    def init(self):
        pass

class File(object):
    """Abstract class for all file operations.

    The `filepath` represents any filepath accessible on the disk.
    The `relapath` is a relative path representative for the archive file.
    The `filename` is the actual filename of the file.
    The `extrpath` determines the extraction path and may be used for read().
    """

    def __init__(self, filepath=None, contents=None, relapath=None,
                 filename=None, mode=None, password=None, description=None,
                 selected=None, stream=None, platforms=None):

        self.filepath = filepath
        self.relapath = relapath
        self.mode = mode
        self.error = None
        self.description = description
        self.password = password
        self.children = []
        self.duplicate = False
        self.unpacker = None
        self.parent = None
        self.preview = True
        self.archive = False
        # Extract the filename from any of the available path components.
        self.filename = ntpath.basename(
            filename or self.relapath or self.filepath or ""
        ).rstrip("\x00") or None
        self._contents = contents
        self._platforms = platforms
        self._selected = selected
        self._human_type = None
        self._extension = None
        self._md5 = None
        self._sha1 = None
        self._sha256 = None
        self._mime = None
        self._magic = None
        self._mime_human = None
        self._magic_human = None
        self._stream = stream
        self._ole = None
        self._ole_tried = False

    @classmethod
    def from_path(self, filepath, relapath=None, filename=None,
                  password=None):
        return File(
            filepath=filepath, stream=open(filepath, "rb"),
            relapath=relapath, filename=filename, password=password
        )

    def temp_path(self, suffix=""):
        # TODO Depending on use-case we may not need a full copy. Perhaps
        # abstract away the "if self.f.filepath ... else ..." logic?
        fd, filepath = tempfile.mkstemp(suffix=suffix)
        shutil.copyfileobj(self.stream, os.fdopen(fd, "wb"))
        return filepath

    @property
    def contents(self):
        if self._contents is None and self.filepath:
            self._contents = open(self.filepath, "rb").read()
        return self._contents

    @property
    def stream(self):
        if not self._stream:
            return io.BytesIO(self.contents)

        self._stream.seek(0)
        return self._stream

    def __identify(self):
        data = identify(self)
        if data:
            self._selected = data[0]
            self._human_type = data[1]
            self._extension = data[2]
            self._platforms = data[3]

    def __hashes(self):
        sha256, s, buf = hashlib.sha256(), self.stream, True
        sha1 = hashlib.sha1()
        md5 = hashlib.md5()
        while buf:
            buf = s.read(0x10000)
            sha256.update(buf)
            md5.update(buf)
            sha1.update(buf)

        self._sha256 = sha256.hexdigest()
        self._sha1 = sha1.hexdigest()
        self._md5 = md5.hexdigest()

    @property
    def md5(self):
        if not self._md5:
            self.__hashes()
        return self._md5

    @property
    def sha1(self):
        if not self._sha1:
            self.__hashes()
        return self._sha1

    @property
    def sha256(self):
        if not self._sha256:
            self.__hashes()
        return self._sha256

    @property
    def magic(self):
        if not self._magic and self.filesize:
            self._magic = magic.from_buffer(self.contents)
        return self._magic or ""

    @property
    def mime(self):
        if not self._mime and self.filesize:
            self._mime = magic.from_buffer(
                self.contents, mime=True
            )
        return self._mime or ""

    @property
    def magic_human(self):
        if not self._magic_human:
            magic = self.magic or ""
            if "," in magic:
                spl = magic.split(",")
                magic = "%s (%s)" % (spl[0], ",".join(spl[1:3]).strip())

            self._magic_human = magic
        return self._magic_human or ""

    @property
    def mime_human(self):
        if not self._mime_human:
            mime = self.mime or ""
            if "/" in mime:
                mime = mime.split("/", 1)[1]

                if mime.startswith("x-"):
                    mime = mime[2:]

                mime = mime.replace("-", " ")

            self._mime_human = mime
        return self._mime_human or ""

    @property
    def parentdirs(self):
        if not self.relapath:
            return []

        dirname = os.path.dirname(self.relapath.replace("\\", "/"))
        return dirname.split("/") if dirname else []

    @property
    def filesize(self):
        s = self.stream
        s.seek(0, os.SEEK_END)
        return s.tell()
    
    @property
    def extension(self):
        if self._extension is None:
            self.__identify()
        return self._extension

    @property
    def human_type(self):
        if self._human_type is None:
            self.__identify()
        return self._human_type

    @property
    def platforms(self):
        if self._platforms is None:
            self.__identify()
        return self._platforms

    @property
    def selected(self):
        if self._selected is None:
            self.__identify()
        return self._selected

    @property
    def extrpath(self):
        ret, child = [], self
        while child.parent:
            ret.insert(0, child.relapath)
            child = child.parent
        return ret

    @property
    def relaname(self):
        if not self.relapath:
            return
        # TODO Strip absolute paths for Windows.
        # TODO Normalize relative paths.
        return self.relapath.lstrip("\\/").rstrip("\x00")

    @property
    def ole(self):
        if not self._ole_tried:
            try:
                self._ole = olefile.OleFileIO(self.stream)
            except IOError:
                pass
            self._ole_tried = True
        return self._ole

    def raise_no_ole(self, message):
        if self.ole is None:
            raise UnpackException(message)

    def to_dict(self, selected_files=None):
        children = []
        for child in self.children:
            children.append(child.to_dict(selected_files))
            if selected_files and child.selected:
                selected_files.append(child)

        return {
            "filename": self.filename,
            "relapath": self.relapath,
            "relaname": self.relaname,
            "filepath": self.filepath,
            "extrpath": self.extrpath,
            "parentdirs": self.parentdirs,
            "duplicate": self.duplicate,
            "size": self.filesize,
            "children": children,
            "type": "container" if self.children else "file",
            "finger": {
                "magic": self.magic,
                "mime": self.mime,
                "mime_human": self.mime_human,
                "magic_human": self.magic_human,
            },
            "password": self.password,
            "human_type": self.human_type,
            "extension": self.extension,
            "sha256": self.sha256,
            "md5": self.md5,
            "sha1": self.sha1,
            "platforms": self.platforms,
            "selected": self.selected,
            "preview": self.preview,
            "error": self.error,
        }

    def astree(self, finger=True, sanitize=False, selected_files=None):
        ret = {
            "duplicate": self.duplicate,
            "password": self.password,
            "human_type": self.human_type,
            "extension": self.extension,
            "filename": self.filename,
            "relapath": self.relapath,
            "relaname": self.relaname,
            "extrpath": self.extrpath,
            "size": self.filesize,
            "platforms": self.platforms,
            "selected": self.selected,
            "type": "container" if self.children else "file",
            "children": [],
            "preview": self.preview,
            "error": self.error,
        }

        if not sanitize:
            ret["filepath"] = self.filepath

        if finger:
            ret["finger"] = {
                "mime": self.mime,
                "mime_human": self.mime_human,
                "magic": self.magic,
                "magic_human": self.magic_human,
            }

        def findentry(entry, name):
            for idx in range(len(entry)):
                if entry[idx]["filename"] == name:
                    return entry[idx]

            entry.append({
                "type": "directory",
                "filename": name,
                "children": [],
                "preview": True,
            })
            return entry[-1]
        for child in self.children:
            entry = ret["children"]
            for part in child.parentdirs:
                entry = findentry(entry, part)["children"]
            if selected_files and child.selected:
                selected_files.append(child)
            entry.append(
                child.astree(
                    finger=finger,
                    sanitize=sanitize,
                    selected_files=selected_files
                )
            )

        return ret

    def extract(self, dirpath, filename=None, preserve=False):
        """Extract one or all files into a directory, note that directory
        hierarchy is by default not preserved with this function."""
        for child in self.children:
            if filename and child.relapath != filename:
                continue

            if not preserve:
                filepath = os.path.join(dirpath, child.filename)
            else:
                filepath = os.path.abspath(os.path.join(
                    dirpath, child.relaname
                ))
                # Avoid path traversal.
                if not filepath.startswith(dirpath):
                    continue
                if not os.path.exists(os.path.dirname(filepath)):
                    os.mkdir(os.path.dirname(filepath))

            shutil.copyfileobj(child.stream, open(filepath, "wb"), 1024*1024)
            child.extract(dirpath, preserve=preserve)

    def read(self, relapath, stream=False):
        """Extract a single file from a possibly nested archive. See also the
        `extrpath` field of an embedded document."""
        if isinstance(relapath, (str, bytes)):
            relapath = relapath,

        relapath, nextpath = relapath[0], relapath[1:]
        for child in self.children:
            if child.relapath == relapath:
                if nextpath:
                    return child.read(nextpath)
                return child.stream if stream else child.contents

    def get_child(self, relaname, regex=False):
        if not regex:
            relaname = "%s$" % re.escape(relaname)

        for child in self.children:
            if child.relaname and re.match(relaname, child.relaname):
                return child
