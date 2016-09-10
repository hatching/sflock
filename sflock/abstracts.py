# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import magic
import hashlib
import os.path
import ntpath
import shutil

import sflock

from sflock.exception import UnpackException
from sflock.pick import picker

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
        return os.path.abspath(os.path.join(
            sflock.__path__[0], "data", "zipjail"
        ))

    def handles(self):
        if picker(self.f) == self.name:
            return True

        if self.magic and self.magic in self.f.magic:
            return True

        return False

    def unpack(self, password=None, duplicates=None):
        raise NotImplementedError

    def process(self, entries, duplicates):
        """Goes through all files and recursively unpacks embedded archives
        if found."""
        ret = []
        duplicates = duplicates or []
        for entry in entries:
            unpacker = picker(entry)
            if unpacker:
                plugin = self.plugins[unpacker](entry)
                if plugin.supported():
                    entry.children = plugin.unpack(duplicates=duplicates)

            if entry.sha256 not in duplicates:
                duplicates.append(entry.sha256)
            else:
                entry.duplicate = True

            ret.append(entry)
        if not ret:
            raise UnpackException("No files unpacked")
        return ret

    def process_directory(self, dirpath, duplicates, password=None):
        """Enumerates a directory, removes the directory, and returns data
        after calling the process function."""
        entries = []
        duplicates = duplicates or []
        for dirpath2, dirnames, filepaths in os.walk(dirpath):
            for filepath in filepaths:
                filepath = os.path.join(dirpath2, filepath)
                f = File.from_path(
                    filepath=filepath,
                    relapath=filepath[len(dirpath)+1:],
                    password=password
                )

                entries.append(f)

        shutil.rmtree(dirpath)
        return self.process(entries, duplicates)

class File(object):
    """Abstract class for all file operations.

    The `filepath` represents any filepath accessible on the disk.
    The `relapath` is a relative path representative for the archive file.
    The `filename` is the actual filename of the file.
    """

    def __init__(self, filepath=None, contents=None, relapath=None,
                 filename=None, mode=None, password=None, description=None,
                 selected=None):
        self.filepath = filepath
        self.relapath = relapath
        self.mode = mode
        self.description = description
        self.password = password
        self.children = []
        self.duplicate = False

        # Extract the filename from any of the available path components.
        self.filename = ntpath.basename(
            filename or self.relapath or self.filepath or ""
        ) or None

        self._contents = contents
        self._selected = selected
        self._sha256 = None
        self._mime = None
        self._magic = None
        self._mime_human = None
        self._magic_human = None

    @classmethod
    def from_path(self, filepath, relapath=None, filename=None,
                  password=None):
        return File(
            filepath=filepath, contents=open(filepath, "rb").read(),
            relapath=relapath, filename=filename, password=password
        )

    @property
    def contents(self):
        if self._contents is None and self.filepath:
            self._contents = open(self.filepath, "rb").read()
        return self._contents

    @property
    def sha256(self):
        if not self._sha256:
            self._sha256 = hashlib.sha256(self.contents or "").hexdigest()
        return self._sha256

    @property
    def magic(self):
        if not self._magic and self.contents:
            self._magic = magic.from_buffer(self.contents)
        return self._magic or ""

    @property
    def mime(self):
        if not self._mime and self.contents:
            self._mime = magic.from_buffer(self.contents, mime=True)
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
        return len(self.contents) if self.contents else 0

    @property
    def package(self):
        filename = self.filename.lower()

        if "DLL" in self.magic:
            if filename.endswith(".cpl"):
                return "cpl"
            # TODO Support PE exports to identify COM objects.
            return "dll"

        if "PE32" in self.magic or "MS-DOS" in self.magic:
            return "exe"

        if "PDF" in self.magic or filename.endswith(".pdf"):
            return "pdf"

        if filename.endswith((".rtf", ".doc", ".docx", ".docm", ".dot",
                              ".dotx", ".docb", ".mht", ".mso")):
            return "doc"

        if filename.endswith((".xls", ".xlsx", ".xlm", ".xlsx", ".xlt",
                              ".xltx", ".xlsm", ".xltm", ".xlsb", ".xla",
                              ".xlam", ".xll", ".xlw")):
            return "xls"

        if filename.endswith((".ppt", ".pptx", ".pps", ".ppsx", ".pptm",
                              ".potm", ".potx", ".ppsm", ".pot", ".ppam",
                              ".sldx", ".sldm")):
            return "ppt"

        if filename.endswith(".pub"):
            return "pub"

        # TODO Get rid of this logic and replace it by actually inspecting
        # the contents of the .zip files (in case of Office 2007+).
        if "Rich Text Format" in self.magic or \
                "Microsoft Word" in self.magic or \
                "Microsoft Office Word" in self.magic:
            return "doc"

        if "Microsoft Office Excel" in self.magic or \
                "Microsoft Excel" in self.magic:
            return "xls"

        if "Microsoft PowerPoint" in self.magic:
            return "ppt"

        if filename.endswith(".jar"):
            return "jar"

        if filename.endswith((".py", ".pyc", ".pyo")):
            return "python"

        if "Python script" in self.magic:
            return "python"

        if filename.endswith(".vbs"):
            return "vbs"

        if filename.endswith((".js", ".jse")):
            return "js"

        if filename.endswith(".msi"):
            return "msi"

        if filename.endswith((".ps1", ".ps1xml", ".psc1", ".psm1")):
            return "ps1"

        if filename.endswith(".wsf"):
            return "wsf"

        if "HTML" in self.magic or filename.endswith((".htm", ".html")):
            return "ie"

    @property
    def selected(self):
        if self._selected is None:
            self._selected = bool(self.package)
        return self._selected

    @selected.setter
    def selected(self, selected):
        self._selected = selected

    def to_dict(self):
        return {
            "filename": self.filename,
            "relapath": self.relapath,
            "filepath": self.filepath,
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
        }

    def astree(self, finger=True):
        ret = {
            "duplicate": self.duplicate,
            "password": self.password,
            "filename": self.filename,
            "relapath": self.relapath,
            "filepath": self.filepath,
            "size": self.filesize,
            "package": self.package,
            "selected": self.selected,
            "type": "container" if self.children else "file",
            "children": [],
        }

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
            })
            return entry[-1]

        for child in self.children:
            entry = ret["children"]
            for part in child.parentdirs:
                entry = findentry(entry, part)["children"]
            entry.append(child.astree(finger=finger))

        return ret
