# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import pytest

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

    @pytest.mark.skip("Skipping, we don't want malware in repo: bde2d06bb333f419fff16376fffce1ee434fa47ca57c4fcb80b2932f86892e40")
    def test_lzip_malware(self):
        assert "lzip compressed data" in f(b"document3230.vbe.lz").magic
        t = LzipFile(f(b"document3230.vbe.lz"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == b"document3230.vbe"
        assert len(files[0].contents) == 748345
        assert "UTF-8 Unicode text, with CRLF line terminators" == files[0].magic
        assert files[0].parentdirs == []
        assert not files[0].selected
