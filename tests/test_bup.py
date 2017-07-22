# Copyright (C) 2016-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.unpack import BupFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_bup_plain():
    assert f("bup_test.bup").magic.startswith((
        "Composite Document File V2", "CDF V2 Document"
    ))
    t = BupFile(f("bup_test.bup"))
    assert t.handles() is True
    assert not t.f.selected
    files = list(t.unpack())

    assert len(files) == 1
    assert not files[0].filepath
    assert files[0].relapath == "efax_9057733019_pdf.zip"
    assert "Zip archive" in files[0].magic
    assert files[0].parentdirs == []
    assert files[0].package is None
    assert files[0].platform is None
    assert not files[0].selected

    assert len(files[0].children) == 1
    assert not files[0].children[0].filepath
    assert files[0].children[0].relapath == "efax_9057733019_pdf.scr"
    assert files[0].children[0].filesize == 377856
    assert files[0].children[0].package == "exe"
    assert files[0].children[0].platform == "windows"
    assert files[0].children[0].selected is True

def test_garbage():
    t = BupFile(f("garbage.bin"))
    assert t.handles() is False
    assert not t.f.selected
    assert not t.unpack()
    assert t.f.mode == "failed"
