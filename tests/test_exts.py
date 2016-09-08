# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.pick import picker

def test_extensions():
    assert picker("") is None
    assert picker(None) is None
    assert picker("a.tar") == "tarfile"
    assert picker("a.tar.gz") == "targzfile"
    assert picker("a.tar.bz2") == "tarbz2file"
    assert picker("a.zip") == "zipfile"
    assert picker("a.rar") == "rarfile"
    assert picker("a.7z") == "7zfile"
    assert picker("a.ace") == "acefile"
    assert picker("a.eml") == "emlfile"
    assert picker("a.msg") == "msgfile"
    assert picker("a.mso") == "msofile"
    assert picker("a.bup") == "bupfile"

def test_case():
    assert picker("A.ZIP") == "zipfile"
