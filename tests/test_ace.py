# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import pytest

from sflock.abstracts import File
from sflock.errors import Errors
from sflock.exception import UnpackException
from sflock.main import unpack
from sflock.unpack import AceFile


def f(filename):
    return File.from_path(os.path.join("tests", "files", filename))


@pytest.mark.skipif("not AceFile(None).supported()")
class TestAceFile(object):
    def test_ace_plain(self):
        assert "ACE archive" in f("ace_plain.ace").magic
        t = AceFile(f("ace_plain.ace"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "ace.txt"
        assert files[0].contents == b"wow .ace"
        assert "ASCII text" in files[0].magic
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_nested_plain(self):
        assert "ACE archive" in f("ace_nested.ace").magic
        t = AceFile(f("ace_nested.ace"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "b00/ace.txt"
        assert files[0].parentdirs == ["b00"]
        assert files[0].contents == b"wow .ace"
        assert not files[0].password
        assert "ASCII text" in files[0].magic
        assert not files[0].selected

    def test_nested2_plain(self):
        assert "ACE archive" in f("ace_nested2.ace").magic
        t = AceFile(f("ace_nested2.ace"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "derp/b00/ace.txt"
        assert files[0].parentdirs == ["derp", "b00"]
        assert files[0].contents == b"wow .ace"
        assert not files[0].password
        assert "ASCII text" in files[0].magic
        assert not files[0].selected

    def test_heuristics(self):
        t = unpack("tests/files/ace_plain.ace", filename="foo")
        assert t.unpacker == "acefile"
        assert t.filename == "foo"

        t = unpack("tests/files/ace_nested.ace", filename="foo")
        assert t.unpacker == "acefile"
        assert t.filename == "foo"

        t = unpack("tests/files/ace_nested2.ace", filename="foo")
        assert t.unpacker == "acefile"
        assert t.filename == "foo"

    def test_doubledot(self):
        files = list(AceFile(f("ace_doubledot.ace")).unpack())
        assert len(files) == 1
        assert files[0].filename == (
            b"Procurement commercial terms & conditions..exe"
        )

    def test_inmemory(self):
        contents = open("tests/files/ace_plain.ace", "rb").read()
        t = unpack(contents=contents)
        assert t.unpacker == "acefile"
        assert t.filename is None
        assert t.filepath is None
        assert len(t.children) == 1

    def test_garbage(self):
        t = AceFile(f("garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        with pytest.raises(UnpackException) as e:
            t.unpack()
        assert e.value.state == Errors.NOTHING_EXTRACTED


@pytest.mark.skipif("AceFile(None).supported()")
def test_noace_plain():
    assert "ACE archive" in f("ace_plain.ace").magic
    t = AceFile(f("ace_plain.ace"))
    assert t.handles() is True
    assert not t.f.selected
