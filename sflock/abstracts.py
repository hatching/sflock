# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

class Unpacker(object):
    """Abstract class for Unpacker engines."""
    name = None
    author = None

    def __init__(self, filepath):
        self.filepath = filepath

    def unpack(self):
        pass

class File(object):
    """Abstract class for extracted files."""
    def __init__(self, filepath, contents):
        self.filepath = filepath
        self.contents = contents
