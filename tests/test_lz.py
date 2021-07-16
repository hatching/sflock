# Copyright (C) 2016-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.main import unpack


def test_embed_lzip():
    t = unpack(b"tests/files/test.vbe.lz.zip")
    assert t.filename == b"test.vbe.lz.zip"
    assert t.children[0].filename == b"document3230.vbe.lz"
    assert t.children[0].children[0].sha256 == "36ef14835a9d2c8fe241286a7758b7f849bdabccc698e7e78318abfb195dc1db"
