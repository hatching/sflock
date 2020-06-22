# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path

from sflock.abstracts import File
from sflock.unpack import MsoFile

def f(filename):
    return File.from_path(os.path.join("tests", "files", filename))

def test_garbage():
    m = MsoFile(f("garbage.bin"))
    assert m.handles() is False
    assert m.f.selected
    assert not m.unpack()
    assert m.f.mode == "failed"
