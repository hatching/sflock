# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import pytest

from sflock.abstracts import File
from sflock.unpack import ZpaqFile


def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))


class TestZpaqFile(object):
    def test_qpaq(self):
        assert "ZPAQ file" in f(b"test.zpaq").magic
        t = ZpaqFile(f(b"test.zpaq"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == b"Zfaggccwnm.exe"
        assert files[0].contents == b"hello world\n"
        assert files[0].magic == "PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows"
        assert files[0].parentdirs == []
