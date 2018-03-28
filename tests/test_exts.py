# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File, Unpacker

def guess(filename):
    return sorted(list(Unpacker.guess(File(filename=filename))))

def test_extensions():
    assert guess(b"a.tar") == ["tarfile"]
    assert guess(b"a.tar.gz") == ["targzfile"]
    assert guess(b"a.tar.bz2") == ["tarbz2file"]
    assert guess(b"a.zip") == ["zipfile"]
    assert guess(b"a.rar") == ["rarfile"]
    assert guess(b"a.7z") == ["7zfile"]
    assert guess(b"a.ace") == ["acefile"]
    assert guess(b"a.eml") == ["emlfile"]
    assert guess(b"a.msg") == ["msgfile"]
    assert guess(b"a.mso") == ["msofile", "office"]
    assert guess(b"a.bup") == ["bupfile"]
    assert guess(b"a.lzh") == ["lzhfile"]
    assert guess(b"a.lha") == ["lzhfile"]

def test_case():
    assert guess(b"A.ZIP") == ["zipfile"]
