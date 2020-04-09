from sflock.main import unpack
import os

path = os.path.join("tests", "files", "extension")

def _help(extension):
    for sample in os.listdir(os.path.join(path, extension)):
        if sample.startswith("."):
            continue
        f = unpack(
            contents=open(
                os.path.join(
                    path, extension, sample
                ), "rb").read()
        )
        try:
            assert f.extension == extension
        except AssertionError:
            raise AssertionError(
                "Sample: %s. Expected: %s, Received: %s" % (
                    sample, extension, f.extension
                )
            )

def test_doc():
    _help("doc")

def test_docx():
    _help("docx")

def test_exe():
    _help("exe")

def test_flv():
    _help("flv")

def test_html():
    _help("html")

def test_hwp():
    _help("hwp")

def test_jar():
    _help("jar")

def test_js():
    _help("js")

def test_mp3():
    _help("mp3")

def test_msi():
    _help("msi")

def test_ods():
    _help("ods")

def test_odt():
    _help("odt")

def test_pdf():
    _help("pdf")

def test_ppt():
    _help("ppt")

def test_pptx():
    _help("pptx")

def test_ps():
    _help("ps")

def test_py():
    _help("py")

def test_rar():
    _help("rar")

def test_rtf():
    _help("rtf")

def test_xls():
    _help("xls")

def test_xlsx():
    _help("xlsx")

