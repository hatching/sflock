# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.main import unpack

def test_elf():
    elf = unpack(b"tests/files/busybox-i686")
    assert elf.package == "generic"
    assert elf.platform == "linux"
