# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import hashlib
import io
import ntpath
import os.path
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import olefile

from sflock.compat import magic
from sflock.config import iter_passwords
from sflock.errors import Errors
from sflock.exception import (
    UnpackException, MaxNestedError, DecryptionFailedError,
    NotSupportedError
)
from sflock.identify import identify
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
    dependency = ""

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
        arg = "--clone=10" if self.name == "7zfile" else "--clone=0"

        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)

        p = subprocess.Popen(
            (zipjail, filepath, dirpath, arg, "--", self.exe) + args,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return_code = p.wait()
        out, err = p.communicate()
        low_err = err.lower()

        if b"excessive writing caused incomplete unpacking!" in low_err:
            raise UnpackException(
                "Cancelled: unpacked archive exceeds maximum size",
                Errors.TOTAL_TOO_LARGE
            )

        if any(x in low_err for x in
               (b"detected potential out-of-path arbitrary overwrite",
                b"Detected potential directory traversal arbitrary overwrite")
        ):

            raise UnpackException(
                "Cancelled: directory traversal attempt detected",
                Errors.CANCELLED_DIR_TRAVERSAL
            )

        if b"blocked system call" in low_err \
                and b"syscall=symlink" in low_err or \
                b"potential symlink-based arbitrary overwrite" in low_err:
            raise UnpackException(
                "Cancelled: symlink creation attempt detected",
                Errors.CANCELLED_SYMLINK
            )

        if any(x in low_err for x in
               (b"wrong password", b"bad password", b"password is incorrect",
                b"password required")):
            raise DecryptionFailedError(
                "No correct password for encrypted archive"
            )

        if b"unknown lstat() errno" in low_err:
            # Handle unknown lstat errors as if the unpacking tool does
            # not supported the current file and allow another unpacker to
            # be chosen.
            raise NotSupportedError(f"Zipjail error: {err}")

        if return_code == 1:
            raise UnpackException(f"Zipjail error: {err}", Errors.ZIPJAIL_FAIL)

        return not return_code

    def handles(self):
        if not self.magic:
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

        if self.f:
            self.f.clear_error()

        ret = []
        for f in entries:
            if f.filename and f.filename.strip() == "":
                continue

            unavailable_plugins = []
            detected_plugins = 0
            for unpacker in Unpacker.guess(f):
                detected_plugins += 1
                plugin = self.plugins[unpacker](f)

                if plugin.supported():
                    depth += 1
                    if depth > MAX_NESTED:
                        raise MaxNestedError(
                            "The submitted file exceeded the maximum of %s "
                            "nested archive files" % MAX_NESTED
                        )

                    try:
                        f.children = plugin.unpack(depth, password, duplicates)

                    except NotSupportedError as e:
                        # This state can occur when a unpacker encounters a
                        # thing it cannot handle that it did not detect during
                        # the 'handles' or 'supported' phase. We let other
                        # unpackers try to unpack the current file after this.
                        f.set_error(Errors.NOT_SUPPORTED, str(e))
                        f.unpacker = unpacker
                        continue

                    except UnpackException as e:
                        state = e.state

                        # Use a default error state if no error state was set
                        if not state:
                            state = Errors.UNPACK_FAILED

                        f.set_error(state, str(e))

                        # Store the unpacker and stop unpacking this file.
                        f.unpacker = unpacker
                        break

                    depth -= 1

                    # TODO Improve this. The following is simply a guesstimate
                    # towards which unpacker is actually used. If there are
                    # multiple unpackers eligible for the current file, but
                    # neither unpacks anything, then f.unpacker will be set to
                    # the last available unpacker.
                    f.unpacker = unpacker
                    if f.children:
                        break
                else:
                    unavailable_plugins.append(plugin)

            if not f.mode and unavailable_plugins and \
                    len(unavailable_plugins) == detected_plugins:
                deps = ', '.join(p.dependency for p in unavailable_plugins)
                err = "One or more unpackers support this file, but the " \
                      f"following dependencies are missing: {deps}"
                f.set_error(Errors.MISSING_DEPENDENCY, err)

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

        if self.f:
            self.f.clear_error()

        if not os.listdir(dirpath):
            shutil.rmtree(dirpath)
            raise UnpackException(
                "Extraction directory was empty", Errors.NOTHING_EXTRACTED
            )

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

        # If a password was provided, first try that.
        insert_at = 0
        if passwords:
            insert_at = 1
        passwords.insert(insert_at, None)

        for password in iter_passwords():
            if password not in passwords:
                passwords.append(password)

        last_error = None
        for password in passwords:
            try:
                return self.decrypt(password, *args, **kwargs)
            except DecryptionFailedError as e:
                last_error = str(e)

        #
        # self.f.set_error(Errors.DECRYPTION_FAILED, last_error)

        raise DecryptionFailedError(last_error, Errors.DECRYPTION_FAILED)
        #return False

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
                 selected=False, stream=None, platforms=[]):


        if isinstance(filepath, Path):
            self.filepath = str(filepath)
        else:
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
        self.archive = False
        self.identified = False
        self.safelisted = False
        self.safelist_reason = ""
        # Extract the filename from any of the available path components.
        self.filename = ntpath.basename(
            filename or self.relapath or self.filepath or ""
        ).rstrip("\x00") or None
        self._contents = contents
        self._platforms = platforms
        self._selected = selected
        self._selectable = selected
        self._identified_ran = False
        self._human_type = ""
        self._extension = ""
        self._dependency_version = ""
        self._dependency = ""
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

    def _identify(self):
        if self._identified_ran:
            return
        self._identified_ran = True
        data = identify(self)
        if data:
            self._selected = data[0]
            self._selectable = data[0]
            self._human_type = data[1]
            self._extension = data[2]
            self._platforms = []
            for platform in data[3]:
                self._platforms.append(
                    {"platform": platform, "os_version": ""}
                )

            self._dependency = data[4]
            self._dependency_version = ""
            self.identified = True

    def _hashes(self):
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
            self._hashes()
        return self._md5

    @property
    def sha1(self):
        if not self._sha1:
            self._hashes()
        return self._sha1

    @property
    def sha256(self):
        if not self._sha256:
            self._hashes()
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
    def dependency(self):
        if not self._identified_ran:
            self._identify()
        return self._dependency

    @property
    def dependency_version(self):
        if not self._identified_ran:
            self._identify()
        return self._dependency_version

    @property
    def extension(self):
        if not self._identified_ran:
            self._identify()
        return self._extension

    @property
    def human_type(self):
        if not self._identified_ran:
            self._identify()
        return self._human_type

    @property
    def platforms(self):
        if not self._identified_ran:
            self._identify()
        return self._platforms

    @property
    def selected(self):
        if not self._identified_ran:
            self._identify()

        if self.error:
            return False

        return self._selected

    @property
    def selectable(self):
        if not self._identified_ran:
            self._identify()

        if self.error:
            return False

        return self._selectable

    @property
    def extrpath(self):
        ret, child = [], self
        while child.parent:
            if not child.relapath:
                return ret

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

    def set_error(self, state, error):
        self.mode = state
        self.error = error

    def clear_error(self):
        self.mode = Errors.NO_ERROR
        self.error = None

    def safelist(self, reason):
        self.safelisted = True
        self.safelist_reason = reason

    def deselect(self):
        self._selected = False

    def unselectable(self):
        self._selected = False
        self._selectable = False

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
            "identified": self.identified,
            "platforms": self.platforms,
            "selected": self.selected,
            "selectable": self.selectable,
            "dependency": self._dependency,
            "dependency_version": self._dependency_version,
            "safelisted": self.safelisted,
            "safelist_reason": self.safelist_reason,
            "error": self.error,
        }

    def astree(self, finger=True, sanitize=False, selected_files=None,
               child_cb=None):
        ret = {
            "duplicate": self.duplicate,
            "password": self.password,
            "human_type": self.human_type,
            "extension": self.extension,
            "dependency": self._dependency,
            "dependency_version": self._dependency_version,
            "filename": self.filename,
            "relapath": self.relapath,
            "relaname": self.relaname,
            "extrpath": self.extrpath,
            "size": self.filesize,
            "identified": self.identified,
            "platforms": self.platforms,
            "selected": self.selected,
            "selectable": self.selectable,
            "safelisted": self.safelisted,
            "safelist_reason": self.safelist_reason,
            "sha256": self.sha256,
            "md5": self.md5,
            "sha1": self.sha1,
            "type": "container" if self.children else "file",
            "children": [],
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

        if child_cb:
            child_cb(self, ret)

        def findentry(entry, name):
            for idx in range(len(entry)):
                if entry[idx]["filename"] == name:
                    return entry[idx]

            entry.append({
                "type": "directory",
                "filename": name,
                "children": []
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
                    selected_files=selected_files,
                    child_cb=child_cb
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
