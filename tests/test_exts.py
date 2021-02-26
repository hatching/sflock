# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path

from sflock.abstracts import File, Unpacker

def guess(file):
    return sorted(list(Unpacker.guess(file)))

def f(filename):
    return File.from_path(os.path.join("tests", "files", filename))

def test_extensions():
    assert guess(f("tar_plain.tar")) == ["tarfile"]
    assert guess(f("tar_plain2.tar.gz")) == ["targzfile"]
    assert guess(f("tar_plain2.tar.bz2")) == ["tarbz2file"]
    assert guess(f("zip_plain.zip")) == ["7zfile", "zipfile"]
    assert guess(f("rar_plain.rar")) == ["rarfile"]
    assert guess(f("7z_plain.7z")) == ["7zfile"]
    assert guess(f("ace_plain.ace")) == ["acefile"]
    assert guess(f("eml_nested_eml.eml")) == ["emlfile"]
    assert guess(f("msg_invoice.msg")) == ["msgfile"]
    assert guess(f("oledata.mso")) == ["msofile"]
    assert "bupfile" in guess(f("bup_test.bup"))
    assert guess(f("test.lzh")) == ["lzhfile"]
    assert guess(f("randomfile.lha")) == ["lzhfile"]
    assert guess(f("gzip1.gzip")) == ["gzipfile", "targzfile"]

def test_case():
    assert guess(f("ZIP_PLAIN.ZIP")) == ["7zfile", "zipfile"]
