# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

def picker(filename):
    """Guesses the unpacker for this file based on its filename extension."""
    if not filename:
        return

    if filename.endswith((".tar", ".tar.gz", ".tar.bz2")):
        return "tarfile"

    if filename.endswith((".zip")):
        return "zipfile"

    if filename.endswith((".rar")):
        return "rarfile"
