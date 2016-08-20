# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import magic
import hashlib
import ntpath
from StringIO import StringIO

from sflock.signatures import Signatures

class Unpacker(object):
    """Abstract class for Unpacker engines."""
    name = None
    author = None

    # Initiated at runtime - contains each Unpacker subclass.
    plugins = {}

    def __init__(self, f):
        self.f = f
        self.init()

    def init(self):
        pass

    def handles(self):
        raise NotImplementedError

    def unpack(self):
        raise NotImplementedError

    def determine(self):
        pass

    def parse_items(self, entries, duplicates):
        tmp_data = []

        for entry in entries.files():
            if entry.filepath.endswith((".gz", ".tar", ".bz2", ".zip", ".tgz")):
                f = File(contents=entry.contents)
                signature = f.get_signature()

                container = self.plugins[signature["unpacker"]](f)
                entry.children = container.unpack(mode=signature["mode"],
                                                  duplicates=duplicates)

            tmp_data.append(entry)

        directories = sorted(entries.directories(),
                             key=lambda entry: entry.filepath.count("/"), reverse=True)

        for directory in directories:
            for file in [e for e in entries.files() \
                         if e.filepath.startswith(directory.filepath)]:
                basepath = file.filepath[len(directory.filepath):]
                if "/" not in basepath and basepath:
                    directory.children.append(file)

            # find parent directory of this directory
            for tmp_directory in directories:
                parent_path = "%s/" % "/".join(directory.filepath.split("/")[:-2])
                if tmp_directory.filepath == parent_path:
                    tmp_directory.children.append(directory)

            tmp_data.append(directory)

        # remove duplicates from root list
        data = []
        for entry in tmp_data:
            if isinstance(entry, Directory):
                if entry.filepath.count("/") == 1:
                    data.append(entry)
            elif isinstance(entry, File):
                if "/" not in entry.filepath:
                    data.append(entry)

        return data

class File(object):
    """Abstract class for extracted files."""

    def __init__(self, filepath=None, contents=None, mode=None, password=None,
                 description=None):
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
        if not self._sha256 and \
            isinstance(self.contents, (str, unicode, bytes)) and \
            len(self.contents) > 0:

            sha256 = hashlib.sha256(StringIO(self.contents).getvalue()).hexdigest()
            if not sha256:
                hash = ""

            self._sha256 = sha256
        else:
            return ""

        return self._sha256

    @property
    def magic(self):
        if not self._finger["magic"] and isinstance(self.contents, (str, unicode, bytes)):
            self._finger["magic"] = magic.from_buffer(self.contents)
        return self._finger["magic"]

    @property
    def mime(self):
        if not self._finger["mime"] and isinstance(self.contents,(str, unicode, bytes)):
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
                magic = "%s (%s)" % (spl[0],
                                     ",".join(spl[1:3]).strip())

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
    def filename(self):
        if not self._filename and not self.filepath.endswith("/"):
            self._filename = ntpath.basename(self.filepath)

        return self._filename

    def to_dict(self):
        if not self.contents:
            size = 0
        else:
            size = len(self.contents)

        return {
            "filepath": self.filepath,
            "filename": self.filename,
            "duplicate": self.duplicate,
            "size": len(self.contents),
            "children": self.children,
            "type": "container" if self.children else "file",
            "finger": {
                "magic": self.magic,
                "mime": self.mime,
                "mime_human": self.mime_human,
                "magic_human": self.magic_human
            },
            "password": self.password,
            "sha256": self.sha256
        }

class Directory(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.children = []

    def to_dict(self):
        return {
            "filepath": self.filepath,
            "filename": ntpath.basename(self.filepath[:-1]),
            "children": self.children,
            "type": "directory"
        }

class Entries(object):
    def __init__(self):
        self.children = []

    def files(self):
        return [z for z in self.children if isinstance(z, File)]

    def directories(self):
        return [z for z in self.children if isinstance(z, Directory)]