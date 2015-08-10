# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import pkg_resources

from sflock.abstracts import File

def iter_passwords():
    filepath = pkg_resources.resource_filename("sflock", "data/password.txt")
    for line in open(filepath, "rb"):
        yield line.strip()

def test_file(filename):
    relative_filename = os.path.join("data", "test", filename)
    filepath = pkg_resources.resource_filename("sflock", relative_filename)
    return File.from_path(filepath)
