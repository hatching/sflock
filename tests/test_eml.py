# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.exception import UnpackException
from sflock.unpack import EmlFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_eml_tar_nested2():
    assert "smtp mail" in f("eml_tar_nested2.eml").magic.lower()
    t = EmlFile(f("eml_tar_nested2.eml"))
    assert t.handles() is True
    files = list(t.unpack())

    assert len(files) == 1
    assert files[0].filepath == "tar_nested2.tar"
    assert "POSIX tar" in files[0].magic

    assert len(files[0].children) == 1
    assert files[0].children[0].contents == "hello world\n"
    assert files[0].children[0].magic == "ASCII text"
    assert files[0].children[0].parentdirs == ["deepfoo", "foo"]

def test_eml_nested_eml():
    assert "MIME entity" in f("eml_nested_eml.eml").magic
    t = EmlFile(f("eml_nested_eml.eml"))
    assert t.handles() is True
    files = list(t.unpack())
    assert len(files) == 2

    assert files[0].filepath == "multipart.eml"
    assert "ASCII text" in files[0].magic
    assert len(files[0].children) == 2

    assert files[0].children[0].filepath == u"\u60e1\u610f\u8edf\u9ad4.doc"
    assert files[0].children[0].filesize == 12
    assert files[0].children[0].package == "doc"

    assert files[0].children[1].filepath == "cuckoo.png"
    assert files[0].children[1].filesize == 11970
    assert files[0].children[1].package is None

    assert files[1].filepath == "att1"
    assert "UTF-8 Unicode" in files[1].magic
    assert files[1].contents == "\xe6\x83\xa1\xe6\x84\x8f\xe8\xbb\x9f\xe9\xab\x94"
    assert files[1].package is None

def test_garbage():
    t = EmlFile(f("garbage.bin"))
    assert t.handles() is False

    with pytest.raises(UnpackException):
        t.unpack()
