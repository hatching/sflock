# Copyright (C) 2017-2020 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os

from sflock.main import unpack

path = os.path.join("tests", "files", "extension")

def _help(extension):
    files = os.listdir(os.path.join(path, extension))
    try:
        files.remove(".gitkeep")
    except ValueError:
        pass
    if len(files) < 1:
        raise ValueError(
            f"Identify test type: '{extension}' has 0 file to test with"
        )
    for sample in files:
        if sample.startswith("."):
            continue
        f = unpack(
            filepath=os.path.join(
                    path, extension, sample
                )
        )

        try:
            assert f.extension == extension
        except AssertionError as e:
            raise AssertionError(
                "Sample: %s. Expected: %s, Received: %s, Magic: %s, Mime: %s" % (
                    sample, extension, f.extension, f.magic, f.mime
                )
            ) from e

def test_7z():
    _help("7z")

def test_ace():
    _help("ace")

def test_apk():
    _help("apk")

def test_bat():
    _help("bat")

def test_cab():
    _help("cab")

def test_daa():
    _help("daa")

def test_dll():
    _help("dll")

def test_doc():
    _help("doc")

def test_docm():
    _help("docm")

def test_docx():
    _help("docx")

def test_dotm():
    _help("dotm")

def test_dotx():
    _help("dotx")

def test_elf():
    _help("elf")

def test_eml():
    _help("eml")

def test_mht():
    _help("mht")

def test_exe():
    _help("exe")

def test_hta():
    _help("hta")

def test_html():
    _help("html")

def test_hwp():
    _help("hwp")

def test_iqy():
    _help("iqy")

def test_iso():
    _help("iso")

def test_jar():
    _help("jar")

def test_js():
    _help("js")

def test_lnk():
    _help("lnk")

def test_msg():
    _help("msg")

def test_msi():
    _help("msi")

def test_ods():
    _help("ods")

def test_odt():
    _help("odt")

def test_pdf():
    _help("pdf")

def test_ppsm():
    _help("ppsm")

def test_ppsx():
    _help("ppsx")

def test_ppt():
    _help("ppt")

def test_pptm():
    _help("pptm")

def test_pptx():
    _help("pptx")

def test_ps1():
    _help("ps1")

def test_py():
    _help("py")

def test_rar():
    _help("rar")

def test_rtf():
    _help("rtf")

def test_slk():
    _help("slk")

def test_txt():
    _help("txt")

def test_url():
    _help("url")

def test_vbs():
    _help("vbs")

def test_wsf():
    _help("wsf")

def test_xls():
    _help("xls")

def test_xlsb():
    _help("xlsb")

def test_xlsm():
    _help("xlsm")

def test_xlam():
    _help("xlam")

def test_xlsx():
    _help("xlsx")
