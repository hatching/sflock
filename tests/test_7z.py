# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import Zip7File

def f(filename):
    return File.from_path("tests/files/%s" % filename)

@pytest.mark.skipif("not Zip7File(None).supported()")
class Test7zFile(object):
    def test_7z_plain(self):
        assert "7-zip archive" in f("7z_plain.7z").magic
        t = Zip7File(f("7z_plain.7z"))
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
        assert "7-zip archive" in f("7z_nested.7z").magic
        t = Zip7File(f("7z_nested.7z"))
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
        assert "7-zip archive" in f("7z_nested2.7z").magic
        t = Zip7File(f("7z_nested2.7z"))
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

    def test_heuristics(self):
        t = unpack("tests/files/7z_plain.7z", filename="foo")
        assert t.unpacker == "7zfile"
        assert t.filename == "foo"

        t = unpack("tests/files/7z_nested.7z", filename="foo")
        assert t.unpacker == "7zfile"
        assert t.filename == "foo"

        t = unpack("tests/files/7z_nested2.7z", filename="foo")
        assert t.unpacker == "7zfile"
        assert t.filename == "foo"

        """
        t = unpack("tests/files/7z_encrypted.7z", filename="foo")
        assert t.unpacker == "7zfile"
        assert t.filename == "foo"
        """

@pytest.mark.skipif("Zip7File(None).supported()")
def test_no7z_plain():
    assert "7-zip archive" in f("7z_plain.7z").magic
    t = Zip7File(f("7z_plain.7z"))
    assert t.handles() is True
    assert not t.unpack()
