# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.exception import UnpackException
from sflock.unpack import MsgFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_msg_embedded():
    assert "Composite Document File V2" in f("msg_invoice.msg").magic
    m = MsgFile(f("msg_invoice.msg"))
    assert m.handles() is True
    files = list(m.unpack())

    assert len(files) == 3
    assert files[0].filepath == "image003.emz"
    assert files[0].filesize == 1137
    assert files[0].package is None

    assert files[1].filepath == "image004.png"
    assert files[1].filesize == 1132
    assert files[1].package is None

    assert files[2].filepath == "oledata.mso"
    assert files[2].filesize == 234898
    assert files[2].package == "doc"

def test_garbage():
    m = MsgFile(f("garbage.bin"))
    assert m.handles() is False

    with pytest.raises(UnpackException):
        m.unpack()
