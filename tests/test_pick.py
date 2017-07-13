# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.main import unpack
from sflock.pick import package

def test_malformed_rtf():
    assert package(File("tests/files/maldoc/0882c8")) == "doc"
    assert package(File("tests/files/maldoc/118368")) == "doc"

def test_lnk():
    f = File(contents=open("tests/files/lnk_1.lnk", "rb").read())
    assert package(f) == "generic"

def test_ole():
    msg = open("tests/files/msg_invoice.msg", "rb").read()
    bup = open("tests/files/bup_test.bup", "rb").read()

    assert unpack(contents=msg).unpacker == "msgfile"
    assert unpack(contents=bup).unpacker == "bupfile"

@pytest.mark.xfail
def test_bup():
    mso = unpack("tests/files/msg_invoice.msg").read("oledata.mso")

    # At the moment we only look at the file extension for .mso files.
    # TODO Allow bruteforcing to identify file type. Note that this is
    # currently not supported as it slows down our unit tests by two (!).
    assert unpack(contents=mso).unpacker == "msofile"
