# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

def picker(filename):
    """Guesses the type of file based on its extension."""
    if not filename:
        return

    if filename.endswith((".tar", ".tar.gz", ".tar.bz2")):
        return "tar"

    if filename.endswith((".zip")):
        return "zip"

    if filename.endswith((".rar")):
        return "rar"
