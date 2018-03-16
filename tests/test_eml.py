# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import mock
import os.path
import pytest
import re

from sflock.abstracts import File
from sflock.unpack import EmlFile

def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))

def test_eml_tar_nested2():
    assert "smtp mail" in f(b"eml_tar_nested2.eml").magic.lower()
    t = EmlFile(f(b"eml_tar_nested2.eml"))
    assert t.handles() is True
    assert not t.f.selected
    files = list(t.unpack())

    assert len(files) == 1
    assert not files[0].filepath
    assert files[0].relapath == b"tar_nested2.tar"
    assert "POSIX tar" in files[0].magic
    assert not files[0].selected

    assert len(files[0].children) == 1
    assert files[0].children[0].contents == b"hello world\n"
    assert files[0].children[0].magic == "ASCII text"
    assert files[0].children[0].parentdirs == [b"deepfoo", b"foo"]
    assert not files[0].children[0].selected

def test_eml_nested_eml():
    assert "MIME entity" in f(b"eml_nested_eml.eml").magic
    t = EmlFile(f(b"eml_nested_eml.eml"))
    assert t.handles() is True
    assert not t.f.selected
    files = list(t.unpack())
    assert len(files) == 2

    assert not files[0].filepath
    assert files[0].relapath == b"multipart.eml"
    assert "ASCII text" in files[0].magic
    assert len(files[0].children) == 2
    assert not files[0].selected

    assert not files[0].children[0].filepath
    assert files[0].children[0].relapath == u"\u60e1\u610f\u8edf\u9ad4.doc"
    assert files[0].children[0].filesize == 12
    assert files[0].children[0].package == "doc"
    assert files[0].children[0].platform == "windows"
    assert files[0].children[0].selected is True

    assert not files[0].children[1].filepath
    assert files[0].children[1].relapath == b"cuckoo.png"
    assert files[0].children[1].filesize == 11970
    assert files[0].children[1].package is None
    assert files[0].children[1].platform is None
    assert not files[0].children[1].selected

    assert files[1].relapath == b"att1"
    assert "UTF-8 Unicode" in files[1].magic
    assert files[1].contents == b"\xe6\x83\xa1\xe6\x84\x8f\xe8\xbb\x9f\xe9\xab\x94"
    assert files[1].package is None
    assert files[1].platform is None
    assert not files[1].selected

def test_faulty_eml():
    assert f(b"eml_faulty.eml_").magic in ("data", "RFC 822 mail text")
    t = EmlFile(f(b"eml_faulty.eml_"))
    assert t.handles() is True
    files = list(t.unpack())
    assert files[0].children[0].filename == b"DOC1820617988-PDF.vbs"
    assert files[0].children[0].filesize == 89851

def test_eml_exception():
    """We must ensure that re.compile is restored at all times."""
    re_compile = re.compile
    EmlFile(f(b"eml_faulty.eml_")).unpack()
    assert re.compile == re_compile

    with mock.patch("email.message_from_string") as p:
        p.side_effect = Exception("test_exception")
        with pytest.raises(Exception) as e:
            EmlFile(f(b"eml_faulty.eml_")).unpack()
        e.match("test_exception")
    assert re.compile == re_compile

def test_garbage():
    t = EmlFile(f(b"garbage.bin"))
    assert t.handles() is False
    assert not t.f.selected
    assert not t.unpack()
