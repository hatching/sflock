# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.unpack import MsoFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_garbage():
    m = MsoFile(f("garbage.bin"))
    assert m.handles() is False
    assert not m.f.selected
    assert not m.unpack()
    assert m.f.mode == "failed"
