# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.pick import picker

def test_extensions():
    assert picker("") is None
    assert picker(None) is None
    assert picker("a.tar") == "tar"
    assert picker("a.tar.gz") == "tar"
    assert picker("a.tar.bz2") == "tar"
    assert picker("a.zip") == "zip"
    assert picker("a.rar") == "rar"
