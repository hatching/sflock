# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.main import supported
from sflock.unpack import AceFile, CabFile, RarFile, Zip7File

def test_supported():
    assert supported()

def test_count_supported():
    count = 9

    if AceFile(None).supported():
        count += 1

    if CabFile(None).supported():
        count += 1

    if RarFile(None).supported():
        count += 1

    if Zip7File(None).supported():
        count += 5

    assert count == len(supported())
