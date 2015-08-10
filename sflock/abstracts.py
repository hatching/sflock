# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import magic
import unittest

class UnitTest(unittest.TestCase):
    """Abstract class for unit tests."""

class Unpacker(object):
    """Abstract class for Unpacker engines."""
    name = None
    author = None

    def __init__(self, f):
        self.f = f

    def handles(self):
        raise NotImplementedError

    def unpack(self):
        raise NotImplementedError

class File(object):
    """Abstract class for extracted files."""
    magic_set = magic.open(magic.MAGIC_NONE)
    magic_set.load()

    def __init__(self, filepath, contents, mode=None, password=None,
                 description=None):
        self.filepath = filepath
        self.contents = contents
        self.mode = mode
        self.password = password
        self.description = description
        self._magic = None

    @classmethod
    def from_path(self, filepath):
        return File(filepath, open(filepath, "rb").read())

    @property
    def magic(self):
        if not self._magic and self.contents:
            self._magic = self.magic_set.buffer(self.contents)
        return self._magic
