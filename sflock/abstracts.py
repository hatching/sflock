# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import magic
import hashlib
import os.path
import ntpath

from sflock.pick import picker
from sflock.signatures import Signatures

class Unpacker(object):
    """Abstract class for Unpacker engines."""
    name = None
    exe = None

    # Initiated at runtime - contains each Unpacker subclass.
    plugins = {}

    def __init__(self, f):
        self.f = f
        self.init()

    def init(self):
        pass

    def supported(self):
        return os.path.exists(self.exe)

    def handles(self):
        raise NotImplementedError

    def unpack(self):
        raise NotImplementedError

    def process(self, entries, duplicates):
        """Goes through all files and recursively unpacks embedded archives
        if found."""
        ret = []
        for entry in entries:
            unpacker = picker(entry.filepath)
            if unpacker:
                plugin = self.plugins[unpacker](entry)
                entry.children = plugin.unpack(duplicates=duplicates)

            ret.append(entry)
        return ret

class File(object):
    """Abstract class for extracted files."""

    def __init__(self, filepath=None, contents=None, mode=None,
                 password=None, description=None):
        self.filepath = filepath
        self.contents = contents
        self.mode = mode
        self.description = description
        self.password = password
        self.children = []
        self.duplicate = False

        self._filename = None
        self._sha256 = None
        self._finger = {
            "mime": None,
            "magic": None,
            "mime_human": None,
            "magic_human": None
        }

    @classmethod
    def from_path(self, filepath):
        return File(filepath, open(filepath, "rb").read())

    def get_signature(self):
        for k, v in Signatures.signatures.iteritems():
            if self.contents.startswith(k):
                return v

    @property
    def sha256(self):
        if not self._sha256:
            self._sha256 = hashlib.sha256(self.contents or "").hexdigest()
        return self._sha256

    @property
    def magic(self):
        if not self._finger["magic"] and self.contents:
            self._finger["magic"] = magic.from_buffer(self.contents)
        return self._finger["magic"]

    @property
    def mime(self):
        if not self._finger["mime"] and self.contents:
            self._finger["mime"] = magic.from_buffer(self.contents, mime=True)
        return self._finger["mime"]

    @property
    def magic_human(self):
        if not self._finger["magic"]:
            self.magic()

        if not self._finger["magic_human"]:
            magic = self.magic
            if "," in magic:
                spl = magic.split(",")
                magic = "%s (%s)" % (spl[0], ",".join(spl[1:3]).strip())

            self._finger["magic_human"] = magic
        return self._finger["magic_human"]

    @property
    def mime_human(self):
        if not self._finger["mime"]:
            self.mime()

        if not self._finger["mime_human"]:
            mime = self.mime
            if "/" in mime:
                mime = mime.split("/", 1)[1]

                if mime.startswith("x-"):
                    mime = mime[2:]

                mime = mime.replace("-", " ")

            self._finger["mime_human"] = mime
        return self._finger["mime_human"]

    @property
    def parentdirs(self):
        dirname = os.path.dirname(self.filepath.replace("\\", "/"))
        return dirname.split("/") if dirname else []

    @property
    def filename(self):
        if not self._filename and not self.filepath.endswith("/"):
            self._filename = ntpath.basename(self.filepath)
        return self._filename

    def to_dict(self):
        return {
            "filepath": self.filepath,
            "parentdirs": self.parentdirs,
            "filename": self.filename,
            "duplicate": self.duplicate,
            "size": len(self.contents) if self.contents else 0,
            "children": self.children,
            "type": "container" if self.children else "file",
            "finger": {
                "magic": self.magic,
                "mime": self.mime,
                "mime_human": self.mime_human,
                "magic_human": self.magic_human,
            },
            "password": self.password,
            "sha256": self.sha256,
        }
