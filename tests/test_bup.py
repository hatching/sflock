# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.exception import UnpackException
from sflock.unpack import BupFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_bup_plain():
    assert "Composite Document File V2" in f("bup_test.bup").magic
    t = BupFile(f("bup_test.bup"))
    assert t.handles() is True
    files = list(t.unpack())

    assert len(files) == 1
    assert files[0].filepath == "efax_9057733019_pdf.zip"
    assert "Zip archive" in files[0].magic
    assert files[0].parentdirs == []
    assert files[0].package is None

    assert len(files[0].children) == 1
    assert files[0].children[0].filepath == "efax_9057733019_pdf.scr"
    assert files[0].children[0].filesize == 377856
    assert files[0].children[0].package == "exe"

def test_garbage():
    t = BupFile(f("garbage.bin"))
    assert t.handles() is False

    with pytest.raises(UnpackException):
        t.unpack()
