# Copyright (C) 2016-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock import unpack


def test_embed_lzip():
    f = unpack(b"tests/files/test.vbe.lz.zip")
    assert f.astree(finger=False) == {
        "children": [
            {
                "children": [
                    {
                        "children": [],
                        "duplicate": False,
                        "error": None,
                        "extrpath": [b"document3230.vbe.lz", b"tmpcxvzmmir.out"],
                        "filename": b"tmpcxvzmmir.out",
                        "filepath": None,
                        "package": None,
                        "password": None,
                        "platform": None,
                        "preview": True,
                        "relaname": b"tmpcxvzmmir.out",
                        "relapath": b"tmpcxvzmmir.out",
                        "selected": False,
                        "size": 748345,
                        "type": "file",
                    }
                ],
                "duplicate": False,
                "error": None,
                "extrpath": [b"document3230.vbe.lz"],
                "filename": b"document3230.vbe.lz",
                "filepath": None,
                "package": None,
                "password": "infected",
                "platform": None,
                "preview": True,
                "relaname": b"document3230.vbe.lz",
                "relapath": b"document3230.vbe.lz",
                "selected": False,
                "size": 2800,
                "type": "container",
            }
        ],
        "duplicate": False,
        "error": None,
        "extrpath": [],
        "filename": b"document3230.vbe.lz.zip",
        "filepath": b"document3230.vbe.lz.zip",
        "package": "zip",
        "password": None,
        "platform": None,
        "preview": False,
        "relaname": None,
        "relapath": None,
        "selected": True,
        "size": 3016,
        "type": "container",
    }
