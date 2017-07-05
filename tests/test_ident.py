# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import tempfile

from sflock.abstracts import File
from sflock.main import unpack

def test_empty():
    fd, filepath = tempfile.mkstemp()
    os.close(fd)
    assert unpack(filepath).package is None

def test_js():
    f = unpack("tests/files/script.js")
    assert f.duplicate is False
    assert f.selected is True
    assert f.package == "js"

def test_wsf():
    f = unpack("tests/files/script.wsf")
    assert f.duplicate is False
    assert f.selected is True
    assert f.package == "wsf"

def test_vba():
    f = unpack("tests/files/script.vbs")
    assert f.duplicate is False
    assert f.selected is True
    assert f.package == "vbs"

def test_ps():
    f = unpack("tests/files/script.ps1")
    assert f.duplicate is False
    assert f.selected is True
    assert f.package == "ps1"

def test_jar():
    f = unpack("tests/files/sample.jar")
    assert f.duplicate is False
    assert f.selected is True
    assert f.preview is False
    assert f.package == "jar"

def test_apk():
    f = unpack("tests/files/sample.apk")
    assert f.duplicate is False
    assert f.selected is True
    assert f.preview is False
    assert f.package == "apk"

def test_ppt():
    f = unpack("tests/files/ppt_1.pptx")
    assert f.duplicate is False
    assert f.preview is False
    assert f.selected is True
    assert f.package == "ppt"
    assert f.get_child("[Content_Types].xml") is not None
    assert len(f.children) == 37

def test_doc1():
    f = unpack("tests/files/doc_1.docx_")
    assert f.duplicate is False
    assert f.selected is True
    assert f.preview is False
    assert f.package == "doc"
    assert f.get_child("[Content_Types].xml") is not None
    assert len(f.children) == 12
    assert f.children[0].selected is False
    assert f.children[4].selected is False
    assert f.children[8].selected is False
    assert f.children[11].selected is False

def test_doc2():
    f = unpack("tests/files/doc_2.xlsx_")
    assert f.duplicate is False
    assert f.selected is True
    assert f.preview is False
    assert f.package == "xls"
    assert f.get_child("[Content_Types].xml") is not None
    assert len(f.children) == 12
    assert f.children[0].selected is False
    assert f.children[11].selected is False

def test_doc3():
    f = unpack("tests/files/maldoc_office.htm")
    assert f.duplicate is False
    assert f.selected is True
    assert f.preview is False
    assert f.package == "doc"

def test_oledoc1():
    f = unpack("tests/files/oledoc1.doc_")
    assert f.package == "doc"
