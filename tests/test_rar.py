# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.exception import UnpackException
from sflock.main import unpack
from sflock.unpack import RarFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

@pytest.mark.skipif("not RarFile(None).supported()")
class TestRarFile:
    def test_plain(self):
        assert "RAR archive" in f("rar_plain.rar").magic
        t = RarFile(f("rar_plain.rar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert files[0].relapath == "bar.txt"
        assert files[0].contents == "hello world\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_nested_plain(self):
        assert "RAR archive" in f("rar_nested.rar").magic
        t = RarFile(f("rar_nested.rar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "foo/bar.txt"
        assert files[0].parentdirs == ["foo"]
        assert files[0].contents == "hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested2_plain(self):
        assert "RAR archive" in f("rar_nested2.rar").magic
        t = RarFile(f("rar_nested2.rar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "deepfoo/foo/bar.txt"
        assert files[0].parentdirs == ["deepfoo", "foo"]
        assert files[0].contents == "hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_rar_encrypted(self):
        assert "RAR archive" in f("sflock_encrypted.rar").magic
        z = RarFile(f("sflock_encrypted.rar"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack("infected"))
        assert len(files) == 1
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == "sflock_encrypted_rar"
        assert files[0].password == "infected"
        assert "ASCII text" in files[0].magic
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_heuristics(self):
        t = unpack("tests/files/rar_plain.rar", filename="foo")
        assert t.unpacker == "rarfile"

        t = unpack("tests/files/rar_nested.rar", filename="foo")
        assert t.unpacker == "rarfile"

        t = unpack("tests/files/rar_nested2.rar", filename="foo")
        assert t.unpacker == "rarfile"

        t = unpack(
            "tests/files/sflock_encrypted.rar",
            filename="foo",
            password="infected"
        )
        assert t.unpacker == "rarfile"

    def test_garbage(self):
        t = RarFile(f("garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected

        with pytest.raises(UnpackException):
            t.unpack()

@pytest.mark.skipif("RarFile(None).supported()")
def test_norar_plain():
    assert "RAR archive" in f("rar_plain.rar").magic
    t = RarFile(f("rar_plain.rar"))
    assert t.handles() is True
    assert not t.f.selected

    with pytest.raises(UnpackException):
        t.unpack()
