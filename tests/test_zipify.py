# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.main import unpack, zipify

def test_zipify1():
    a = unpack("tests/files/tar_plain.tar")
    b = unpack("foo.zip", zipify(a))
    assert len(a.children) == len(b.children)
    assert a.children[0].relapath == b.children[0].relapath
    assert a.children[0].contents == b.children[0].contents

def test_zipify2():
    a = unpack("tests/files/zip_nested.zip")
    b = unpack("foo.zip", zipify(a))
    assert len(a.children) == len(b.children)
    assert a.children[0].relapath == b.children[0].relapath
    assert a.children[0].contents == b.children[0].contents

@pytest.mark.skipif("not Zip7File(None).supported()")
def test_zipify3():
    a = unpack("tests/files/7z_nested2.7z")
    b = unpack("foo.zip", zipify(a))
    assert len(a.children) == len(b.children)
    assert a.children[0].relapath == b.children[0].relapath
    assert a.children[0].contents == b.children[0].contents

def test_zipify4():
    a = unpack("tests/files/tar_plain2.tar")
    b = unpack("foo.zip", zipify(a))
    assert len(a.children) == len(b.children)
    assert a.children[0].relapath == b.children[0].relapath
    assert a.children[0].contents == b.children[0].contents
    assert a.children[1].relapath == b.children[1].relapath
    assert a.children[1].contents == b.children[1].contents
