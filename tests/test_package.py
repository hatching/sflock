# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File


def test_package():
    assert File(filename=b"a.pdf").package == "pdf"
    assert File(filename=b"a.rtf").package == "doc"
    assert File(filename=b"a.doc").package == "doc"
    assert File(filename=b"a.docx").package == "doc"
    assert File(filename=b"a.docm").package == "doc"
    assert File(filename=b"a.dot").package == "doc"
    assert File(filename=b"a.dotx").package == "doc"
    assert File(filename=b"a.docb").package == "doc"
    assert File(filename=b"a.mht").package == "ie"
    assert File(filename=b"a.mhtml").package == "ie"
    assert File(filename=b"a.mso").package == "doc"
    assert File(filename=b"a.xls").package == "xls"
    assert File(filename=b"a.xlsx").package == "xls"
    assert File(filename=b"a.xlm").package == "xls"
    assert File(filename=b"a.xlsx").package == "xls"
    assert File(filename=b"a.xlt").package == "xls"
    assert File(filename=b"a.xltx").package == "xls"
    assert File(filename=b"a.xlsm").package == "xls"
    assert File(filename=b"a.xltm").package == "xls"
    assert File(filename=b"a.xlsb").package == "xls"
    assert File(filename=b"a.xla").package == "xls"
    assert File(filename=b"a.xlam").package == "xls"
    assert File(filename=b"a.xll").package == "xls"
    assert File(filename=b"a.xlw").package == "xls"
    assert File(filename=b"a.ppt").package == "ppt"
    assert File(filename=b"a.pptx").package == "ppt"
    assert File(filename=b"a.pps").package == "ppt"
    assert File(filename=b"a.ppsx").package == "ppt"
    assert File(filename=b"a.pptm").package == "ppt"
    assert File(filename=b"a.potm").package == "ppt"
    assert File(filename=b"a.potx").package == "ppt"
    assert File(filename=b"a.ppsm").package == "ppt"
    assert File(filename=b"a.pot").package == "ppt"
    assert File(filename=b"a.ppam").package == "ppt"
    assert File(filename=b"a.sldx").package == "ppt"
    assert File(filename=b"a.sldm").package == "ppt"
    assert File(filename=b"a.pub").package == "pub"
    assert File(filename=b"a.jar").package == "jar"
    assert File(filename=b"a.py").package == "python"
    assert File(filename=b"a.pyc").package == "python"
    assert File(filename=b"a.pyo").package == "python"
    assert File(filename=b"a.vbs").package == "vbs"
    assert File(filename=b"a.js").package == "js"
    assert File(filename=b"a.jse").package == "jse"
    assert File(filename=b"a.msi").package == "msi"
    assert File(filename=b"a.ps1").package == "ps1"
    assert File(filename=b"a.ps1xml").package == "ps1"
    assert File(filename=b"a.psc1").package == "ps1"
    assert File(filename=b"a.psm1").package == "ps1"
    assert File(filename=b"a.wsf").package == "wsf"
    assert File(filename=b"a.wsc").package == "wsf"
    assert File(filename=b"a.htm").package == "ie"
    assert File(filename=b"a.html").package == "html"
    assert File(filename=b"a.bat").package == "generic"
    assert File(filename=b"a.cmd").package == "generic"
    assert File(filename=b"a.lnk").package == "generic"
    assert File(filename=b"a.hta").package == "ie"
    assert File(filename=b"a.sh").package == "generic"


def test_case():
    assert File(filename=b"A.PDF").package == "pdf"
    assert File(filename=b"A.RTF").package == "doc"
    assert File(filename=b"A.DOC").package == "doc"
    assert File(filename=b"A.PUB").package == "pub"
    assert File(filename=b"A.JAR").package == "jar"


def test_platform():
    assert File(filename=b"a.pdf").platform is None
    assert File(filename=b"a.rtf").platform == "windows"
    assert File(filename=b"a.doc").platform == "windows"
    assert File(filename=b"a.docx").platform == "windows"
    assert File(filename=b"a.docm").platform == "windows"
    assert File(filename=b"a.dot").platform == "windows"
    assert File(filename=b"a.dotx").platform == "windows"
    assert File(filename=b"a.docb").platform == "windows"
    assert File(filename=b"a.mht").platform == "windows"
    assert File(filename=b"a.mhtml").platform == "windows"
    assert File(filename=b"a.mso").platform == "windows"
    assert File(filename=b"a.xls").platform == "windows"
    assert File(filename=b"a.xlsx").platform == "windows"
    assert File(filename=b"a.xlm").platform == "windows"
    assert File(filename=b"a.xlsx").platform == "windows"
    assert File(filename=b"a.xlt").platform == "windows"
    assert File(filename=b"a.xltx").platform == "windows"
    assert File(filename=b"a.xlsm").platform == "windows"
    assert File(filename=b"a.xltm").platform == "windows"
    assert File(filename=b"a.xlsb").platform == "windows"
    assert File(filename=b"a.xla").platform == "windows"
    assert File(filename=b"a.xlam").platform == "windows"
    assert File(filename=b"a.xll").platform == "windows"
    assert File(filename=b"a.xlw").platform == "windows"
    assert File(filename=b"a.ppt").platform == "windows"
    assert File(filename=b"a.pptx").platform == "windows"
    assert File(filename=b"a.pps").platform == "windows"
    assert File(filename=b"a.ppsx").platform == "windows"
    assert File(filename=b"a.pptm").platform == "windows"
    assert File(filename=b"a.potm").platform == "windows"
    assert File(filename=b"a.potx").platform == "windows"
    assert File(filename=b"a.ppsm").platform == "windows"
    assert File(filename=b"a.pot").platform == "windows"
    assert File(filename=b"a.ppam").platform == "windows"
    assert File(filename=b"a.sldx").platform == "windows"
    assert File(filename=b"a.sldm").platform == "windows"
    assert File(filename=b"a.pub").platform == "windows"
    assert File(filename=b"a.jar").platform is None
    assert File(filename=b"a.py").platform is None
    assert File(filename=b"a.pyc").platform is None
    assert File(filename=b"a.pyo").platform is None
    assert File(filename=b"a.vbs").platform == "windows"
    assert File(filename=b"a.js").platform is None
    assert File(filename=b"a.jse").platform is None
    assert File(filename=b"a.msi").platform == "windows"
    assert File(filename=b"a.ps1").platform == "windows"
    assert File(filename=b"a.ps1xml").platform == "windows"
    assert File(filename=b"a.psc1").platform == "windows"
    assert File(filename=b"a.psm1").platform == "windows"
    assert File(filename=b"a.wsf").platform == "windows"
    assert File(filename=b"a.wsc").platform == "windows"
    assert File(filename=b"a.htm").platform == "windows"
    # assert File(filename=b"a.html").platform == "windows"
    assert File(filename=b"a.bat").platform == "windows"
    assert File(filename=b"a.cmd").platform == "windows"
    assert File(filename=b"a.lnk").platform == "windows"
    assert File(filename=b"a.hta").platform == "windows"
    assert File(filename=b"a.sh").platform == "linux"
