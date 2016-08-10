# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pkg_resources

def iter_passwords():
    filepath = pkg_resources.resource_filename("sflock", "data/password.txt")
    for line in open(filepath, "rb"):
        yield line.strip()
