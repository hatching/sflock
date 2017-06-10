# Copyright (C) 2015-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import hashlib
import io
import ntpath
import os.path
import re
import shutil
import tempfile

from sflock.compat import magic
from sflock.misc import data_file
from sflock.pick import package

class Unpacker(object):
    """Abstract class for Unpacker engines."""
    name = None
    exe = None
    exts = []
    magic = None

    # Initiated at runtime - contains each Unpacker subclass.
    plugins = {}

    def __init__(self, f):
        self.f = f
        self.init()

    def init(self):
        pass

    def supported(self):
        return os.path.exists(self.exe)

    @property
    def zipjail(self):
        return data_file("zipjail.elf")

    def handles(self):
        if self.f.filename and self.f.filename.lower().endswith(self.exts):
            return True

        if self.magic and self.magic in self.f.magic:
            return True

        return False

    @staticmethod
    def guess(f):
        """Guesses the unpacker based on the filename and/or contents."""
        for plugin in Unpacker.plugins.values():
            if plugin(f).handles():
                return plugin.name

    def unpack(self, password=None, duplicates=None):
        raise NotImplementedError

    def process(self, entries, duplicates):
        """Recursively unpacks embedded archives if found."""
        if duplicates is None:
            duplicates = []

        ret = []
        for f in entries:
            f.unpacker = Unpacker.guess(f)
            if f.unpacker:
                plugin = self.plugins[f.unpacker](f)
                if plugin.supported():
                    f.children = plugin.unpack(duplicates=duplicates)

            if f.sha256 not in duplicates:
                duplicates.append(f.sha256)
            else:
                f.duplicate = True

            f.parent = self.f
            ret.append(f)
        return ret

    def process_directory(self, dirpath, duplicates, password=None):
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
                f = File(
                    relapath=filepath[len(dirpath)+1:],
                    password=password,
                    contents=open(filepath, "rb").read()
                )

                entries.append(f)

        shutil.rmtree(dirpath)
        return self.process(entries, duplicates)

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
                 selected=None, stream=None):
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

        # Extract the filename from any of the available path components.
        self.filename = ntpath.basename(
            filename or self.relapath or self.filepath or ""
        ).rstrip("\x00") or None

        self._contents = contents
        self._package = None
        self._selected = selected
        self._sha256 = None
        self._mime = None
        self._magic = None
        self._mime_human = None
        self._magic_human = None
        self._stream = stream

    @classmethod
    def from_path(self, filepath, relapath=None, filename=None,
                  password=None):
        return File(
            filepath=filepath, stream=open(filepath, "rb"),
            relapath=relapath, filename=filename, password=password
        )

    def temp_path(self, suffix=""):
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

    @property
    def sha256(self):
        if not self._sha256:
            h, s, buf = hashlib.sha256(), self.stream, True
            while buf:
                buf = s.read(0x10000)
                h.update(buf)

            self._sha256 = h.hexdigest()
        return self._sha256

    @property
    def magic(self):
        if not self._magic and self.filesize:
            self._magic = magic.from_buffer(self.stream.read(1024*1024))
        return self._magic or ""

    @property
    def mime(self):
        if not self._mime and self.filesize:
            self._mime = magic.from_buffer(
                self.stream.read(1024*1024), mime=True
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
    def package(self):
        if self._package is None:
            self._package = package(self)
        return self._package

    @package.setter
    def package(self, value):
        self._package = value

    @property
    def selected(self):
        if self._selected is None:
            self._selected = bool(self.package)
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

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

    def to_dict(self):
        return {
            "filename": self.filename,
            "relapath": self.relapath,
            "relaname": self.relaname,
            "filepath": self.filepath,
            "extrpath": self.extrpath,
            "parentdirs": self.parentdirs,
            "duplicate": self.duplicate,
            "size": self.filesize,
            "children": [child.to_dict() for child in self.children],
            "type": "container" if self.children else "file",
            "finger": {
                "magic": self.magic,
                "mime": self.mime,
                "mime_human": self.mime_human,
                "magic_human": self.magic_human,
            },
            "password": self.password,
            "sha256": self.sha256,
            "package": self.package,
            "selected": self.selected,
            "preview": self.preview,
        }

    def astree(self, finger=True, sanitize=False):
        ret = {
            "duplicate": self.duplicate,
            "password": self.password,
            "filename": self.filename,
            "relapath": self.relapath,
            "relaname": self.relaname,
            "extrpath": self.extrpath,
            "size": self.filesize,
            "package": self.package,
            "selected": self.selected,
            "type": "container" if self.children else "file",
            "children": [],
            "preview": self.preview,
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
            for idx in xrange(len(entry)):
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
            entry.append(child.astree(finger=finger, sanitize=sanitize))

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
        if isinstance(relapath, basestring):
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
