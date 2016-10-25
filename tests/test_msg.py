# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import hashlib

from sflock.abstracts import File
from sflock.unpack import MsgFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_msg_embedded():
    assert f("msg_invoice.msg").magic.startswith((
        "Composite Document File V2", "CDF V2 Document"
    ))
    m = MsgFile(f("msg_invoice.msg"))
    assert m.handles() is True
    assert not m.f.selected
    files = list(m.unpack())

    assert len(files) == 3
    assert files[0].relapath == "image003.emz"
    assert files[0].filesize == 1137
    assert files[0].package is None
    assert not files[0].children
    assert not files[0].selected

    assert files[1].relapath == "image004.png"
    assert files[1].filesize == 1132
    assert files[1].package is None
    assert not files[1].children
    assert not files[1].selected

    assert files[2].relapath == "oledata.mso"
    assert files[2].filesize == 234898
    assert files[2].package == "doc"
    assert files[2].selected is True

    assert len(files[2].children) == 1
    assert files[2].children[0].relapath == "Firefox Setup Stub 43.0.1.exe"
    assert files[2].children[0].filesize == 249336
    assert files[2].children[0].selected is False

    assert hashlib.md5(
        files[2].children[0].contents
    ).hexdigest() == "c8cd8eb88f1848cf456725d67baaaa35"

def test_garbage():
    m = MsgFile(f("garbage.bin"))
    assert m.handles() is False
    assert not m.f.selected
    assert not m.unpack()
    assert m.f.mode == "failed"
