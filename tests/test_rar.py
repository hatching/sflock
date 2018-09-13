# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import pytest

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import RarFile

def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))

@pytest.mark.skipif("not RarFile(None).supported()")
class TestRarFile:
    def test_plain(self):
        assert "RAR archive" in f(b"rar_plain.rar").magic
        t = RarFile(f(b"rar_plain.rar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == b"bar.txt"
        assert files[0].contents == b"hello world\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_nested_plain(self):
        assert "RAR archive" in f(b"rar_nested.rar").magic
        t = RarFile(f(b"rar_nested.rar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == b"foo/bar.txt"
        assert files[0].parentdirs == [b"foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested2_plain(self):
        assert "RAR archive" in f(b"rar_nested2.rar").magic
        t = RarFile(f(b"rar_nested2.rar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == b"deepfoo/foo/bar.txt"
        assert files[0].parentdirs == [b"deepfoo", b"foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_rar_encrypted(self):
        assert "RAR archive" in f(b"sflock_encrypted.rar").magic
        z = RarFile(f(b"sflock_encrypted.rar"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack(b"infected"))
        assert len(files) == 1
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_encrypted_rar"
        assert files[0].password == b"infected"
        assert "ASCII text" in files[0].magic
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_heuristics(self):
        t = unpack(b"tests/files/rar_plain.rar", filename=b"foo")
        assert t.unpacker == "rarfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/rar_nested.rar", filename=b"foo")
        assert t.unpacker == "rarfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/rar_nested2.rar", filename=b"foo")
        assert t.unpacker == "rarfile"
        assert t.filename == b"foo"

        t = unpack(
            b"tests/files/sflock_encrypted.rar",
            filename=b"foo",
            password=b"infected"
        )
        assert t.unpacker == "rarfile"
        assert t.filename == b"foo"

    def test_symlink(self):
        t = unpack(b"tests/files/symlink.rar")
        assert t.unpacker == "rarfile"
        assert t.error == "malicious_symlink"

    def test_inmemory(self):
        contents = open(b"tests/files/rar_plain.rar", "rb").read()
        t = unpack(contents=contents)
        assert t.unpacker == "rarfile"
        assert t.filename is None
        assert t.filepath is None
        assert len(t.children) == 1

    def test_garbage(self):
        t = RarFile(f(b"garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert not t.unpack()
        assert t.f.mode == "failed"

    def test_garbage2(self):
        t = RarFile(f(b"rar_garbage.rar"))
        assert t.handles() is True
        assert not t.f.selected
        files = t.unpack()
        assert len(files) == 1
        assert not files[0].children
        assert files[0].mode == "failed"

@pytest.mark.skipif("RarFile(None).supported()")
def test_norar_plain():
    assert "RAR archive" in f(b"rar_plain.rar").magic
    t = RarFile(f(b"rar_plain.rar"))
    assert t.handles() is True
    assert not t.f.selected
