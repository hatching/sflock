# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import os.path
import zipfile

from sflock.abstracts import File
from sflock.unpack import PdfFile, ZipFile

def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))

def test_pdf_embedded():
    assert f(b"pdf_docm.pdf").magic.startswith("PDF document")
    m = PdfFile(f(b"pdf_docm.pdf"))
    assert m.handles() is True
    assert m.f.selected
    files = list(m.unpack())
    assert not m.f.preview
    assert m.f.package == "pdf"

    assert len(files) == 1
    assert not files[0].filepath
    assert files[0].filename == b"Q6TCWXPS.docm"
    assert files[0].filesize == 55494
    assert files[0].package == "doc"
    assert not files[0].selected
    assert len(files[0].children) == 18

def test_pdf_magic():
    m = PdfFile(File(contents=f(b"pdf_docm.pdf").contents))
    assert m.handles() is True

def test_pdf_is_embedded():
    buf = io.BytesIO()
    z = zipfile.ZipFile(buf, "w")
    z.write("tests/files/pdf_docm.pdf")
    z.close()
    m = ZipFile(File(contents=buf.getvalue()))
    files = list(m.unpack())
    assert len(files) == 1
    assert files[0].package == "pdf"
    assert len(files[0].children) == 1
    assert files[0].children[0].package == "doc"

def test_garbage():
    m = PdfFile(f(b"garbage.bin"))
    assert m.handles() is False
    assert not m.f.selected
    assert not m.unpack()
