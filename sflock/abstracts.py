# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import magic
import hashlib
from StringIO import StringIO

class Unpacker(object):
    """Abstract class for Unpacker engines."""
    name = None
    author = None

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

    def parse_item(self, entry):
        data = {"file": entry}

        if entry.filepath.endswith((".gz", ".tar", ".tar.gz", ".bz2", ".zip")):
            f = File(contents=entry.contents)
            signature = f.get_signature()

            container = signature["unpacker"](f=f)
            data.update({
                "unpacked": [z for z in container.unpack(mode=signature["mode"])]
            })

        return data

class File(object):
    """Abstract class for extracted files."""

    def __init__(self, filepath=None, contents=None, mode=None, password=None,
                 description=None):
        self.filepath = filepath
        self.contents = contents
        self.mode = mode
        self.password = password
        self.description = description
        self._magic = None
        self._magic_mime = None
        self._hash = None

    @classmethod
    def from_path(self, filepath):
        return File(filepath, open(filepath, "rb").read())

    def get_signature(self):
        from sflock.unpack.signatures import Signatures

        for k, v in Signatures.signatures.iteritems():
            if self.contents.startswith(k):
                return v

    @property
    def hash(self):
        if not self._hash and self.contents:
            self._hash = hashlib.sha256(StringIO(self.contents).getvalue()).hexdigest()
        return self._hash

    @property
    def magic(self):
        if not self._magic and self.contents:
            self._magic = magic.from_buffer(self.contents)
        return self._magic

    @property
    def mime(self):
        if not self._magic_mime and self.contents:
            self._magic_mime = magic.from_buffer(self.contents, mime=True)
        return self._magic_mime

    def to_dict(self):
        return {
            "filepath": self.filepath,
            "size": len(self.contents),
            "mode": self.mode,
            "password": self.password,
            "description": self.description,
            "magic": self._magic,
            "mime": self.mime,
            "hash": self.hash
        }
