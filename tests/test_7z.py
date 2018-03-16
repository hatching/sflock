# Copyright (C) 2015-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import hashlib
import pytest

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import Zip7File

def f(filename):
    return File.from_path(b"tests/files/%s" % filename)

@pytest.mark.skipif("not Zip7File(None).supported()")
class Test7zFile(object):
    def test_7z_plain(self):
        assert "7-zip archive" in f(b"7z_plain.7z").magic
        t = Zip7File(f(b"7z_plain.7z"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "bar.txt"
        assert files[0].contents == b"hello world\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_nested_plain(self):
        assert "7-zip archive" in f("7z_nested.7z").magic
        t = Zip7File(f("7z_nested.7z"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "foo/bar.txt"
        assert files[0].parentdirs == ["foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested2_plain(self):
        assert "7-zip archive" in f("7z_nested2.7z").magic
        t = Zip7File(f("7z_nested2.7z"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "deepfoo/foo/bar.txt"
        assert files[0].parentdirs == ["deepfoo", "foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_inmemory(self):
        contents = open("tests/files/7z_plain.7z", "rb").read()
        t = unpack(contents=contents)
        assert t.unpacker == "7zfile"
        assert t.filename is None
        assert t.filepath is None
        assert len(t.children) == 1

    def test_gzip_file(self):
        t = unpack(contents=open("tests/files/gzip1.gzip", "rb").read())
        assert t.unpacker == "gzipfile"
        assert len(t.children) == 1
        assert len(t.children[0].contents) == 801792

    """
    def test_zip_encrypted(self):
        assert "7-zip archive" in f("7z_encrypted.7z").magic
        z = Zip7File(f("7z_encrypted.7z"))
        assert z.handles() is True
        assert not t.f.selected
        files = list(z.unpack("infected"))
        assert len(files) == 1
        assert files[0].relapath == "bar.txt"
        assert files[0].contents == "hello world\n"
        assert files[0].password == "infected"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected
    """

    def test_garbage(self):
        t = Zip7File(f("garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert not t.unpack()
        assert t.f.mode == "failed"

    def test_garbage2(self):
        t = Zip7File(f("7z_garbage.7z"))
        assert t.handles() is True
        assert not t.f.selected
        files = t.unpack()
        assert len(files) == 1
        assert not files[0].children
        assert files[0].mode == "failed"

    def test_heuristics(self):
        t = unpack(b"tests/files/7z_plain.7z", filename="foo")
        assert t.unpacker == "7zfile"
        assert t.filename == "foo"

        t = unpack(b"tests/files/7z_nested.7z", filename="foo")
        assert t.unpacker == "7zfile"
        assert t.filename == "foo"

        t = unpack(b"tests/files/7z_nested2.7z", filename="foo")
        assert t.unpacker == "7zfile"
        assert t.filename == "foo"

        """
        t = unpack(b"tests/files/7z_encrypted.7z", filename="foo")
        assert t.unpacker == "7zfile"
        assert t.filename == "foo"
        """

    def test_payment_iso(self):
        t = Zip7File(f("payment.iso"))
        assert t.handles() is True
        assert not t.f.selected
        files = t.unpack()
        assert len(files) == 1
        assert hashlib.md5(files[0].contents).hexdigest() == (
            "eccd7c33037181277ae23f3c3b5baf74"
        )
        assert not files[0].children
        assert files[0].relaname == (
            "payment slip and bank confirmation document.exe"
        )
        assert files[0].selected is True
        assert files[0].duplicate is False

@pytest.mark.skipif("Zip7File(None).supported()")
def test_no7z_plain():
    assert "7-zip archive" in f(b"7z_plain.7z").magic
    t = Zip7File(f(b"7z_plain.7z"))
    assert t.handles() is True
