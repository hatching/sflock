# Copyright (C) 2015-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import ZipFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

class TestZipfile(object):
    def test_zip_plain(self):
        assert "Zip archive" in f("zip_plain.zip").magic
        z = ZipFile(f("zip_plain.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == "sflock_plain_zip\n"
        assert files[0].password is None
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_zip_encrypted(self):
        assert "Zip archive" in f("zip_encrypted.zip").magic
        z = ZipFile(f("zip_encrypted.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == "sflock_encrypted_zip\n"
        assert files[0].password == "infected"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_zip_encrypted2(self):
        assert "Zip archive" in f("zip_encrypted2.zip").magic
        z = ZipFile(f("zip_encrypted2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1
        assert files[0].mode == "failed"
        assert files[0].description == "Error decrypting file"
        assert files[0].magic is ""
        assert files[0].parentdirs == []
        assert not files[0].selected

        z = ZipFile(f("zip_encrypted2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack("sflock"))
        assert len(files) == 1
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == "sflock_encrypted_zip\n"
        assert files[0].password == "sflock"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_nested(self):
        assert "Zip archive" in f("zip_nested.zip").magic
        z = ZipFile(f("zip_nested.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1

        assert files[0].relapath == "foo/bar.txt"
        assert files[0].parentdirs == ["foo"]
        assert files[0].contents == "hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested2(self):
        assert "Zip archive" in f("zip_nested2.zip").magic
        z = ZipFile(f("zip_nested2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1

        assert files[0].relapath == "deepfoo/foo/bar.txt"
        assert files[0].parentdirs == ["deepfoo", "foo"]
        assert files[0].contents == "hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_heuristics(self):
        t = unpack("tests/files/zip_plain.zip", filename="foo")
        assert t.unpacker == "zipfile"
        assert t.filename == "foo"

        t = unpack("tests/files/zip_nested.zip", filename="foo")
        assert t.unpacker == "zipfile"
        assert t.filename == "foo"

        t = unpack("tests/files/zip_nested2.zip", filename="foo")
        assert t.unpacker == "zipfile"
        assert t.filename == "foo"

        t = unpack("tests/files/zip_encrypted.zip", filename="foo")
        assert t.unpacker == "zipfile"
        assert t.filename == "foo"

        t = unpack("tests/files/zip_encrypted2.zip", filename="foo")
        assert t.unpacker == "zipfile"
        assert t.filename == "foo"

    def test_garbage(self):
        t = ZipFile(f("garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert not t.unpack()
        assert t.f.mode == "failed"

    def test_garbage2(self):
        t = ZipFile(f("zip_garbage.zip"))
        assert t.handles() is True
        assert not t.f.selected
        files = t.unpack()
        assert len(files) == 1
        assert not files[0].children
        assert files[0].mode == "failed"
