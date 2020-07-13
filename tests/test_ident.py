# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import tempfile

from sflock.main import unpack

def test_empty():
    fd, filepath = tempfile.mkstemp()
    os.close(fd)
    assert unpack(filepath).extension == ""
    assert unpack(filepath).platforms == ()

def test_identify():
    f = unpack(contents=open("tests/files/sample.jar", "rb").read())
    assert f.extension == "jar"

    f = unpack(contents=open("tests/files/sample.apk", "rb").read())
    assert f.extension == "apk"

def test_ppt():
    f = unpack(contents=open("tests/files/ppt_1.pptx", "rb").read())
    assert f.duplicate is False
    assert f.selected == False
    assert f.extension == "zip" # based on magic/mime ..
    assert f.platforms == ('windows', 'darwin', 'linux', 'android', 'ios')
    assert f.get_child("[Content_Types].xml") is not None
    assert len(f.children) == 37

def test_doc1():
    f = unpack("tests/files/doc_1.docx_")
    assert f.duplicate is False
    assert f.selected is True
    assert f.extension == "thmx"
    assert f.platforms == ('windows', 'darwin', 'linux', 'android', 'ios')
    assert f.get_child("[Content_Types].xml") is not None
    assert len(f.children) == 12
    assert f.children[0].selected == True
    assert f.children[4].selected == False
    assert f.children[8].selected == False
    assert f.children[11].selected == False

def test_doc2():
    f = unpack("tests/files/doc_2.xlsx_")
    assert f.duplicate is False
    assert f.selected is True
    assert f.extension == "xlsm"
    assert f.platforms == ('windows', 'darwin', 'linux', 'android', 'ios')
    assert f.get_child("[Content_Types].xml") is not None
    assert len(f.children) == 12
    assert f.children[0].selected == True
    assert f.children[11].selected == False

def test_oledoc1():
    f = unpack("tests/files/oledoc1.doc_")
    assert f.extension == "doc"
    assert f.platforms == ('windows', 'darwin', 'linux', 'android', 'ios')

def test_url():
    f = unpack("tests/files/1.url")
    assert f.extension == "txt"
    assert f.platforms == ('windows', 'darwin', 'linux', 'android', 'ios')

def test_slk():
    f = unpack("tests/files/1.slk")
    assert f.extension == "slk"
    assert f.platforms == ('windows', 'darwin', 'linux', 'android', 'ios')

def test_iqy():
    f = unpack("tests/files/1.iqy")
    assert f.extension == "iqy"
    assert f.platforms == ('windows', 'darwin', 'linux', 'android', 'ios')
