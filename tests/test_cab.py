# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import CabFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

@pytest.mark.skipif("not CabFile(None).supported()")
class TestCabFile(object):
    def test_cab2(self):
        assert "Microsoft Cabinet archive" in f("cab2.cab").magic
        t = CabFile(f("cab2.cab"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "Seamark Quotation.exe"
        assert files[0].filesize == 792376
        assert "PE32" in files[0].magic
        assert files[0].parentdirs == []
        assert files[0].selected is True

    def test_heuristics(self):
        t = unpack("tests/files/cab2.cab", filename="foo")
        assert t.unpacker == "cabfile"
        assert t.filename == "foo"

        t = unpack("tests/files/readelf.cab", filename="foo")
        assert t.unpacker == "cabfile"
        assert t.filename == "foo"

    def test_inmemory(self):
        contents = open("tests/files/cab2.cab", "rb").read()
        t = unpack(contents=contents)
        assert t.unpacker == "cabfile"
        assert t.filename is None
        assert t.filepath is None
        assert len(t.children) == 1

    def test_garbage(self):
        t = CabFile(f("garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert not t.unpack()
        assert t.f.mode == "failed"

@pytest.mark.skipif("CabFile(None).supported()")
def test_nocab_plain():
    assert "Microsoft Cabinet archive" in f("cab2.cab").magic
    t = CabFile(f("cab2.cab"))
    assert t.handles() is True
    assert not t.f.selected
