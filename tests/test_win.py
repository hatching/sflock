# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import pytest

from sflock.abstracts import File
from sflock.unpack import WimFile


def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))


class TestWINFile(object):
    @pytest.mark.skip("Skipping, we don't want malware in repo: f7501360eadfb326a0568535dd1c134f5e0febccbe4d0168c0ea902c940855f3")
    def test_lzip_malware(self):
        assert "Windows imaging (WIM)" in f(b"test.win").magic
        t = WimFile(f(b"test.win"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == b"Invoice_for_part_shipped(Feb 19,2021).exe"
        assert len(files[0].contents) == 633344
        assert "PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows" == files[0].magic
        assert files[0].parentdirs == []
        assert files[0].selected
