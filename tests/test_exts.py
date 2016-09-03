# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.pick import picker

def test_extensions():
    assert picker("") is None
    assert picker(None) is None
    assert picker("a.tar") == "tarfile"
    assert picker("a.tar.gz") == "tarfile"
    assert picker("a.tar.bz2") == "tarfile"
    assert picker("a.zip") == "zipfile"
    assert picker("a.rar") == "rarfile"
