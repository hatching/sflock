# Copyright (C) 2018 Hatching B.V>
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import pytest

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import DaaFile

def f(filename):
    return File.from_path(os.path.join("tests", "files", filename))

@pytest.mark.skipif("not DaaFile(None).supported()")
class TestDaaFile(object):
    def test_daa(self):
        assert "PowerISO Direct-Access-Archive" in f("quota.daa").magic
        t = DaaFile(f("quota.daa"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "Revised-Quote.exe"
        assert files[0].filesize == 791040
        assert "PE32" in files[0].magic
        assert files[0].parentdirs == []
        assert files[0].selected is True
