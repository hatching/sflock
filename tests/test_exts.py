# Copyright (C) 2015-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File, Unpacker

def guess(filename):
    return sorted(list(Unpacker.guess(File(filename=filename))))

def test_extensions():
    assert guess("a.tar") == ["tarfile"]
    assert guess("a.tar.gz") == ["targzfile"]
    assert guess("a.tar.bz2") == ["tarbz2file"]
    assert guess("a.zip") == ["zipfile"]
    assert guess("a.rar") == ["rarfile"]
    assert guess("a.7z") == ["7zfile"]
    assert guess("a.ace") == ["acefile"]
    assert guess("a.eml") == ["emlfile"]
    assert guess("a.msg") == ["msgfile"]
    assert guess("a.mso") == ["msofile", "office"]
    assert guess("a.bup") == ["bupfile"]
    assert guess("a.lzh") == ["lzhfile"]

def test_case():
    assert guess("A.ZIP") == ["zipfile"]
