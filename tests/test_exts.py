# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.pick import picker

def test_extensions():
    assert picker(File("a.tar")) == "tarfile"
    assert picker(File("a.tar.gz")) == "targzfile"
    assert picker(File("a.tar.bz2")) == "tarbz2file"
    assert picker(File("a.zip")) == "zipfile"
    assert picker(File("a.rar")) == "rarfile"
    assert picker(File("a.7z")) == "7zfile"
    assert picker(File("a.ace")) == "acefile"
    assert picker(File("a.eml")) == "emlfile"
    assert picker(File("a.msg")) == "msgfile"
    assert picker(File("a.mso")) == "msofile"
    assert picker(File("a.bup")) == "bupfile"

def test_case():
    assert picker(File("A.ZIP")) == "zipfile"
