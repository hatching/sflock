# Copyright (C) 2016-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import hashlib
import io
import zipfile

from sflock import unpack, zipify
from sflock.abstracts import File
from sflock.unpack import MsgFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_msg_embedded():
    assert f("msg_invoice.msg").magic.startswith((
        "Composite Document File V2", "CDF V2 Document", "CDFV2 Microsoft",
    ))
    m = MsgFile(f("msg_invoice.msg"))
    assert m.handles() is True
    assert not m.f.selected
    files = list(m.unpack())

    assert len(files) == 3
    assert not files[0].filepath
    assert files[0].relapath == "image003.emz"
    assert files[0].filesize == 1137
    assert files[0].package is None
    assert not files[0].children
    assert not files[0].selected

    assert not files[1].filepath
    assert files[1].relapath == "image004.png"
    assert files[1].filesize == 1132
    assert files[1].package is None
    assert not files[1].children
    assert not files[1].selected

    assert not files[2].filepath
    assert files[2].relapath == "oledata.mso"
    assert files[2].filesize == 234898
    assert files[2].package == "doc"
    assert files[2].platform == "windows"
    assert files[2].selected is True

    assert len(files[2].children) == 1
    assert not files[2].children[0].filepath
    assert files[2].children[0].relapath == "Firefox Setup Stub 43.0.1.exe"
    assert files[2].children[0].filesize == 249336
    assert files[2].children[0].selected is False

    assert hashlib.md5(
        files[2].children[0].contents
    ).hexdigest() == "c8cd8eb88f1848cf456725d67baaaa35"

def test_msg_nullbyte():
    f = unpack("tests/files/ole_nullbyte.zip")
    assert len(f.children) == 1
    assert len(f.children[0].children) == 2

    ole = f.children[0]
    assert ole.filename == "You have recevied a message.msg"
    assert f.read(ole.extrpath) == ole.contents

    doc = ole.children[0]
    assert doc.filename == "eFax_document-4631559.doc"
    assert doc.relapath == "eFax_document-4631559.doc\x00"
    assert doc.relaname == "eFax_document-4631559.doc"

    z = zipfile.ZipFile(io.BytesIO(zipify(ole)))
    assert z.read(doc.relaname) == doc.contents

def test_msg_doc_magic():
    f = unpack("tests/files/msg_doc.msg_")
    assert len(f.children) == 1
    assert f.children[0].filename == "Kristina_Meyer.doc"
    assert f.children[0].filesize == 57856

def test_msg_rtf_magic():
    f = unpack("tests/files/msg_rtf.msg_")
    assert len(f.children) == 1
    assert f.children[0].filename == "g94ys83xi8_8fb0ud5,7.rtf"
    assert f.children[0].filesize == 138638

def test_garbage():
    m = MsgFile(f("garbage.bin"))
    assert m.handles() is False
    assert not m.f.selected
    assert not m.unpack()
    assert m.f.mode == "failed"
