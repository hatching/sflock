# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

class Unpacker(object):
    """Abstract class for Unpacker engines."""
    name = None
    author = None

    def __init__(self, filepath):
        self.filepath = filepath

    def handles(self):
        raise NotImplementedError

    def unpack(self):
        raise NotImplementedError

class File(object):
    """Abstract class for extracted files."""
    def __init__(self, filepath, contents, mode=None, password=None,
                 description=None):
        self.filepath = filepath
        self.contents = contents
        self.mode = mode
        self.password = password
        self.description = description
