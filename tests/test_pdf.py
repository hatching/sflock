# Copyright (C) 2016-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.unpack import PdfFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_pdf_embedded():
    assert f("pdf_docm.pdf").magic.startswith("PDF document")
    m = PdfFile(f("pdf_docm.pdf"))
    assert m.handles() is True
    assert m.f.selected
    files = list(m.unpack())
    assert not m.f.preview

    assert len(files) == 1
    assert not files[0].filepath
    assert files[0].filename == "Q6TCWXPS.docm"
    assert files[0].filesize == 55494
    assert files[0].package == "doc"
    assert not files[0].selected
    assert len(files[0].children) == 18

def test_garbage():
    m = PdfFile(f("garbage.bin"))
    assert m.handles() is False
    assert not m.f.selected
    assert not m.unpack()
