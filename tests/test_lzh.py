# Copyright (C) 2016-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import LzhFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

@pytest.mark.skipif("not LzhFile(None).supported()")
class TestLzhFile(object):
    def test_lzh_plain(self):
        assert "LHa (" in f("test.lzh").magic
        t = LzhFile(f("test.lzh"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "MICROTECH%20PRECISION%20ENGINEERING.exe"
        assert "PE32 executable (GUI) Intel 80386, for MS Windows" == files[0].magic
        assert files[0].parentdirs == []
        assert not files[0].selected
