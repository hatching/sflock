# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.exception import IncorrectUsageException
from sflock.main import supported, unpack
from sflock.unpack import AceFile, CabFile, RarFile, Zip7File

def test_supported():
    assert supported()

def test_count_supported():
    return
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

def test_unpack_py3():
    with pytest.raises(IncorrectUsageException):
        unpack(filepath="filepath")

    with pytest.raises(IncorrectUsageException):
        unpack(contents="contents")

    with pytest.raises(IncorrectUsageException):
        unpack(password="password")

    with pytest.raises(IncorrectUsageException):
        unpack(filename="filename")

    # It works, but no children are extracted from this Python file.
    assert not unpack(__file__.encode()).children
