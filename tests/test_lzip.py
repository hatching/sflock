# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
from sflock.main import unpack
from sflock.abstracts import File
from sflock.unpack import LzipFile


def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))


class TestLzipFile(object):
    def test_lzip_plain(self):
        assert "lzip compressed data" in f(b"test.lz").magic
        t = LzipFile(f(b"test.lz"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == b"test"
        assert files[0].contents == b"lzip tester\n"
        assert "ASCII text" in files[0].magic
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_embed_lzip(self):
        t = unpack(b"tests/files/test.vbe.lz.zip")
        assert t.filename == b"test.vbe.lz.zip"
        assert t.children[0].filename == b"document3230.vbe.lz"
        assert t.children[0].children[0].sha256 == "36ef14835a9d2c8fe241286a7758b7f849bdabccc698e7e78318abfb195dc1db"
