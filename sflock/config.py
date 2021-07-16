# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

# By default we don't accept a collection of files to be larger than 1GB.
# May be tweaked in the future including modifying this at runtime.
MAX_TOTAL_SIZE = 1024 * 1024 * 1024


def iter_passwords():
    import pkg_resources

    filepath = pkg_resources.resource_filename("sflock", "data/password.txt")
    for line in open(filepath, "rb"):
        yield line.strip()
