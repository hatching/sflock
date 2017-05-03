# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.pick import package

def test_malformed_rtf():
    assert package(File("tests/files/maldoc/0882c8")) == "doc"
    assert package(File("tests/files/maldoc/118368")) == "doc"

def test_lnk():
    f = File(contents=open("tests/files/lnk_1.lnk", "rb").read())
    assert package(f) == "generic"
