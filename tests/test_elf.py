# Copyright (C) 2015-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.main import unpack


def test_elf():
    elf = unpack("tests/files/busybox-i686")
    assert elf.package == "generic"
    assert elf.platform == "linux"
