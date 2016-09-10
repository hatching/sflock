# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File, Unpacker

def test_extensions():
    assert Unpacker.guess(File(filename="a.tar")) == "tarfile"
    assert Unpacker.guess(File(filename="a.tar.gz")) == "targzfile"
    assert Unpacker.guess(File(filename="a.tar.bz2")) == "tarbz2file"
    assert Unpacker.guess(File(filename="a.zip")) == "zipfile"
    assert Unpacker.guess(File(filename="a.rar")) == "rarfile"
    assert Unpacker.guess(File(filename="a.7z")) == "7zfile"
    assert Unpacker.guess(File(filename="a.ace")) == "acefile"
    assert Unpacker.guess(File(filename="a.eml")) == "emlfile"
    assert Unpacker.guess(File(filename="a.msg")) == "msgfile"
    assert Unpacker.guess(File(filename="a.mso")) == "msofile"
    assert Unpacker.guess(File(filename="a.bup")) == "bupfile"

def test_case():
    assert Unpacker.guess(File(filename="A.ZIP")) == "zipfile"
