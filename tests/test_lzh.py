# Copyright (C) 2018 Jurriaan Bremer.
# Copyright (C) 2019 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import pytest

from sflock.abstracts import File
from sflock.unpack import LzhFile


def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))


@pytest.mark.skipif("not LzhFile(None).supported()")
class TestLzhFile(object):
    def test_lzh_plain(self):
        assert "LHa (" in f(b"test.lzh").magic
        t = LzhFile(f(b"test.lzh"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == b"MICROTECH%20PRECISION%20ENGINEERING.exe"
        assert len(files[0].contents) == 652288
        assert "PE32 executable" in files[0].magic
        assert not files[0].parentdirs
        assert files[0].selected is True
