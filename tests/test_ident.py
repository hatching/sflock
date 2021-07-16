# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import tempfile

from sflock.abstracts import File
from sflock.ident import identify
from sflock.main import unpack


def test_empty():
    fd, filepath = tempfile.mkstemp()
    os.close(fd)
    assert unpack(filepath.encode()).package is None
    assert unpack(filepath.encode()).platform is None


def test_identify():
    assert identify(File(b"tests/files/script.js")) == "js"
    assert identify(File(b"tests/files/script.wsf")) == "wsf"
    assert identify(File(b"tests/files/script.vbs")) == "vbs"
    assert identify(File(b"tests/files/script.ps1")) == "ps1"
    f = unpack(contents=open("tests/files/sample.jar", "rb").read())
    assert f.package == "jar"
    f = unpack(contents=open("tests/files/sample.apk", "rb").read())
    assert f.package == "apk"
    assert identify(File(b"tests/files/maldoc_office.htm")) == "doc"
    assert identify(File(b"tests/files/maldoc.xls")) == "xls"
    assert identify(File(b"tests/files/test.hta_")) == "hta"


def test_ppt():
    f = unpack(contents=open("tests/files/ppt_1.pptx", "rb").read())
    assert f.duplicate is False
    assert f.preview is False
    assert f.selected is True
    assert f.package == "ppt"
    assert f.platform == "windows"
    assert f.get_child(b"[Content_Types].xml") is not None
    assert len(f.children) == 37


def test_doc1():
    f = unpack(b"tests/files/doc_1.docx_")
    assert f.duplicate is False
    assert f.selected is True
    assert f.preview is False
    assert f.package == "doc"
    assert f.platform == "windows"
    assert f.get_child(b"[Content_Types].xml") is not None
    assert len(f.children) == 12
    assert f.children[0].selected is False
    assert f.children[4].selected is False
    assert f.children[8].selected is False
    assert f.children[11].selected is False


def test_doc2():
    f = unpack(b"tests/files/doc_2.xlsx_")
    assert f.duplicate is False
    assert f.selected is True
    assert f.preview is False
    assert f.package == "xls"
    assert f.platform == "windows"
    assert f.get_child(b"[Content_Types].xml") is not None
    assert len(f.children) == 12
    assert f.children[0].selected is False
    assert f.children[11].selected is False


def test_oledoc1():
    f = unpack(b"tests/files/oledoc1.doc_")
    assert f.package == "doc"
    assert f.platform == "windows"


def test_url():
    f = unpack(b"tests/files/1.url")
    assert f.package == "ie"
    assert f.platform == "windows"


def test_slk():
    f = unpack(b"tests/files/1.slk")
    assert f.package == "xls"
    assert f.platform == "windows"


def test_iqy():
    f = unpack(b"tests/files/1.iqy")
    assert f.package == "xls"
    assert f.platform == "windows"
