# Copyright (C) 2016-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import os.path
import tempfile
import zipfile

from sflock.main import unpack, supported


def test_unpack1():
    f = unpack(b"tests/files/tar_plain.tar")
    assert len(f.children) == 1
    assert f.children[0].contents == b"sflock_plain_tar\n"


def test_unpack2():
    f = unpack(b"tests/files/tar_nested.tar.bz2")
    assert len(f.children) == 1
    f = f.children[0]
    assert len(f.children) == 1
    assert f.children[0].relapath == b"foo/bar.txt"
    assert f.children[0].relaname == b"foo/bar.txt"
    assert f.children[0].contents == b"hello world\n"


def test_unpack3():
    f = unpack(b"tests/files/zip_nested2.zip")
    assert len(f.children) == 1
    assert f.children[0].relapath == b"deepfoo/foo/bar.txt"
    assert f.children[0].relaname == b"deepfoo/foo/bar.txt"
    assert f.children[0].contents == b"hello world\n"


def test_unpack4():
    f = unpack(b"hoi.txt", b"hello world")
    assert not f.children


def test_astree1():
    f = unpack(b"tests/files/zip_nested2.zip")
    assert f.astree(finger=False) == {
        "children": [
            {
                "children": [
                    {
                        "children": [
                            {
                                "children": [],
                                "duplicate": False,
                                "error": None,
                                "extrpath": [b"deepfoo/foo/bar.txt"],
                                "filename": b"bar.txt",
                                "filepath": None,
                                "package": None,
                                "password": "infected",
                                "platform": None,
                                "preview": True,
                                "relaname": b"deepfoo/foo/bar.txt",
                                "relapath": b"deepfoo/foo/bar.txt",
                                "selected": False,
                                "size": 12,
                                "type": "file",
                            }
                        ],
                        "filename": b"foo",
                        "preview": True,
                        "type": "directory",
                    }
                ],
                "filename": b"deepfoo",
                "preview": True,
                "type": "directory",
            }
        ],
        "duplicate": False,
        "error": None,
        "extrpath": [],
        "filename": b"zip_nested2.zip",
        "filepath": b"tests/files/zip_nested2.zip",
        "package": "zip",
        "password": None,
        "platform": None,
        "preview": False,
        "relaname": None,
        "relapath": None,
        "selected": True,
        "size": 496,
        "type": "container",
    }


def test_astree2():
    f = unpack(b"tests/files/eml_tar_nested2.eml")
    assert f.astree(finger=False) == {
        "children": [
            {
                "children": [
                    {
                        "children": [
                            {
                                "children": [
                                    {
                                        "children": [],
                                        "duplicate": False,
                                        "error": None,
                                        "extrpath": [b"tar_" b"nest" b"ed2." b"tar", b"deep" b"foo/" b"foo/" b"bar." b"txt"],
                                        "filename": b"bar.txt",
                                        "filepath": None,
                                        "package": None,
                                        "password": None,
                                        "platform": None,
                                        "preview": True,
                                        "relaname": b"deepfoo/" b"foo/bar." b"txt",
                                        "relapath": b"deepfoo/" b"foo/bar." b"txt",
                                        "selected": False,
                                        "size": 12,
                                        "type": "file",
                                    }
                                ],
                                "filename": b"foo",
                                "preview": True,
                                "type": "directory",
                            }
                        ],
                        "filename": b"deepfoo",
                        "preview": True,
                        "type": "directory",
                    }
                ],
                "duplicate": False,
                "error": None,
                "extrpath": [b"tar_nested2.tar"],
                "filename": b"tar_nested2.tar",
                "filepath": None,
                "package": "tar",
                "password": None,
                "platform": None,
                "preview": False,
                "relaname": b"tar_nested2.tar",
                "relapath": b"tar_nested2.tar",
                "selected": True,
                "size": 10240,
                "type": "container",
            }
        ],
        "duplicate": False,
        "error": None,
        "extrpath": [],
        "filename": b"eml_tar_nested2.eml",
        "filepath": b"tests/files/eml_tar_nested2.eml",
        "package": None,
        "password": None,
        "platform": None,
        "preview": True,
        "relaname": None,
        "relapath": None,
        "selected": False,
        "size": 15035,
        "type": "container",
    }


def test_astree3():
    f = unpack(b"tests/files/eml_nested_eml.eml")
    assert f.astree(finger=False) == {
        "duplicate": False,
        "filename": b"eml_nested_eml.eml",
        "relapath": None,
        "relaname": None,
        "filepath": b"tests/files/eml_nested_eml.eml",
        "extrpath": [],
        "package": "eml",
        "platform": None,
        "selected": True,
        "preview": False,
        "password": None,
        "size": 24607,
        "error": None,
        "type": "container",
        "children": [
            {
                "duplicate": False,
                "filename": b"multipart.eml",
                "relapath": b"multipart.eml",
                "relaname": b"multipart.eml",
                "filepath": None,
                "extrpath": [
                    b"multipart.eml",
                ],
                "package": None,
                "platform": None,
                "selected": False,
                "preview": True,
                "password": None,
                "size": 17482,
                "error": None,
                "type": "container",
                "children": [
                    {
                        "duplicate": False,
                        "filename": "\u60e1\u610f\u8edf\u9ad4.doc".encode("utf-8"),
                        "relapath": "\u60e1\u610f\u8edf\u9ad4.doc".encode("utf-8"),
                        "relaname": "\u60e1\u610f\u8edf\u9ad4.doc".encode("utf-8"),
                        "filepath": None,
                        "extrpath": [
                            b"multipart.eml",
                            "\u60e1\u610f\u8edf\u9ad4.doc".encode("utf-8"),
                        ],
                        "package": "doc",
                        "platform": "windows",
                        "selected": True,
                        "preview": True,
                        "password": None,
                        "size": 12,
                        "error": None,
                        "type": "file",
                        "children": [],
                    },
                    {
                        "duplicate": False,
                        "filename": b"cuckoo.png",
                        "relapath": b"cuckoo.png",
                        "relaname": b"cuckoo.png",
                        "filepath": None,
                        "extrpath": [
                            b"multipart.eml",
                            b"cuckoo.png",
                        ],
                        "package": None,
                        "platform": None,
                        "selected": False,
                        "preview": True,
                        "password": None,
                        "size": 11970,
                        "error": None,
                        "type": "file",
                        "children": [],
                    },
                ],
            },
            {
                "duplicate": True,
                "filename": b"att1",
                "relapath": b"att1",
                "relaname": b"att1",
                "filepath": None,
                "extrpath": [
                    b"att1",
                ],
                "package": None,
                "platform": None,
                "selected": False,
                "preview": True,
                "password": None,
                "size": 12,
                "error": None,
                "type": "file",
                "children": [],
            },
        ],
    }


def test_astree4():
    f = unpack(b"tests/files/msg_invoice.msg")
    assert f.astree(finger=False) == {
        "children": [
            {
                "children": [
                    {
                        "children": [],
                        "duplicate": False,
                        "error": None,
                        "extrpath": [b"image003.emz", b"output"],
                        "filename": b"output",
                        "filepath": None,
                        "package": None,
                        "password": None,
                        "platform": None,
                        "preview": True,
                        "relaname": b"output",
                        "relapath": b"output",
                        "selected": False,
                        "size": 10352,
                        "type": "file",
                    }
                ],
                "duplicate": False,
                "error": None,
                "extrpath": [b"image003.emz"],
                "filename": b"image003.emz",
                "filepath": None,
                "package": "gzip",
                "password": None,
                "platform": None,
                "preview": False,
                "relaname": b"image003.emz",
                "relapath": b"image003.emz",
                "selected": True,
                "size": 1137,
                "type": "container",
            },
            {
                "children": [],
                "duplicate": False,
                "error": None,
                "extrpath": [b"image004.png"],
                "filename": b"image004.png",
                "filepath": None,
                "package": None,
                "password": None,
                "platform": None,
                "preview": True,
                "relaname": b"image004.png",
                "relapath": b"image004.png",
                "selected": False,
                "size": 1132,
                "type": "file",
            },
            {
                "children": [
                    {
                        "children": [],
                        "duplicate": False,
                        "error": None,
                        "extrpath": [b"oledata.mso", b"Firefox Setup Stub 43.0.1.exe"],
                        "filename": b"Firefox Setup Stub 43.0.1.exe",
                        "filepath": None,
                        "package": "exe",
                        "password": None,
                        "platform": "windows",
                        "preview": True,
                        "relaname": b"Firefox Setup Stub 43.0.1.exe",
                        "relapath": b"Firefox Setup Stub 43.0.1.exe",
                        "selected": False,
                        "size": 249336,
                        "type": "file",
                    }
                ],
                "duplicate": False,
                "error": None,
                "extrpath": [b"oledata.mso"],
                "filename": b"oledata.mso",
                "filepath": None,
                "package": "doc",
                "password": None,
                "platform": "windows",
                "preview": False,
                "relaname": b"oledata.mso",
                "relapath": b"oledata.mso",
                "selected": True,
                "size": 234898,
                "type": "container",
            },
        ],
        "duplicate": False,
        "error": None,
        "extrpath": [],
        "filename": b"msg_invoice.msg",
        "filepath": b"tests/files/msg_invoice.msg",
        "package": None,
        "password": None,
        "platform": None,
        "preview": True,
        "relaname": None,
        "relapath": None,
        "selected": False,
        "size": 270848,
        "type": "container",
    }


def test_astree_sanitize():
    f = unpack(b"tests/files/msg_invoice.msg")
    obj = f.astree(sanitize=False)
    assert "filepath" in obj
    assert "filepath" in obj["children"][0]
    assert "filepath" in obj["children"][1]
    assert "filepath" in obj["children"][2]
    assert "filepath" in obj["children"][2]["children"][0]

    obj = f.astree(sanitize=True)
    assert "filepath" not in obj
    assert "filepath" not in obj["children"][0]
    assert "filepath" not in obj["children"][1]
    assert "filepath" not in obj["children"][2]
    assert "filepath" not in obj["children"][2]["children"][0]


def test_extract1():
    dirpath = tempfile.gettempdir().encode()
    tmpdir = tempfile.gettempdir().encode()
    unpack(b"tests/files/tar_plain.tar").extract(dirpath)
    filepath = os.path.join(tmpdir, b"sflock.txt")
    assert open(filepath, "rb").read() == b"sflock_plain_tar\n"


def test_extract2():
    tmpdir = tempfile.gettempdir().encode()
    unpack(b"tests/files/zip_nested2.zip").extract(tmpdir)
    filepath = os.path.join(tmpdir, b"bar.txt")
    assert open(filepath, "rb").read() == b"hello world\n"


def test_extract3():
    dirpath = tempfile.mkdtemp().encode()
    f = unpack(b"tests/files/bup_test.bup").children[0]

    f.extract(dirpath, b"404.exe")
    assert not os.path.exists(os.path.join(dirpath, b"404.exe"))
    assert not os.path.exists(os.path.join(dirpath, b"efax_9057733019_pdf.scr"))

    f.extract(dirpath, b"efax_9057733019_pdf.scr")
    filepath = os.path.join(dirpath, b"efax_9057733019_pdf.scr")
    assert len(open(filepath, "rb").read()) == 377856


def test_extract4_nopreserve():
    buf = io.BytesIO()
    z = zipfile.ZipFile(buf, "w")
    z.writestr("thisisfilename", "B" * 1024)
    z.close()
    f = unpack(contents=buf.getvalue().replace(b"thisisfilename", b"/absolute/path"))
    dirpath = tempfile.mkdtemp(prefix=b"sfl")
    f.extract(dirpath, preserve=True)

    filepath = os.path.join(dirpath, b"absolute", b"path")
    assert os.path.exists(filepath)
    assert open(filepath, "rb").read() == b"B" * 1024


def test_extract5_relative():
    buf = io.BytesIO()
    z = zipfile.ZipFile(buf, "w")
    z.writestr("foobarfilename", "A" * 1024)
    z.writestr("thisisfilename", "B" * 1024)
    z.close()
    f = unpack(contents=buf.getvalue().replace(b"thisisfilename", b"/../../../rela"))
    dirpath = tempfile.mkdtemp(prefix=b"sfl")
    f.extract(dirpath, preserve=True)
    assert len(os.listdir(dirpath)) == 2

    filepath = os.path.join(dirpath, b"foobarfilename")
    assert open(filepath, "rb").read() == b"A" * 1024


def test_duplicate():
    duplicates = []
    f1 = unpack(b"tests/files/tar_plain.tar", duplicates=duplicates)
    f2 = unpack(b"tests/files/tar_plain.tar", duplicates=duplicates)
    assert f1.children[0].duplicate is False
    assert f2.children[0].duplicate is True


def test_read1():
    f = unpack(b"tests/files/bup_test.bup")
    assert len(f.read(b"efax_9057733019_pdf.zip")) == 212663
    assert (
        len(
            f.read(
                [
                    b"efax_9057733019_pdf.zip",
                    b"efax_9057733019_pdf.scr",
                ]
            )
        )
        == 377856
    )


def test_read2():
    f = unpack(b"tests/files/msg_invoice.msg")
    assert len(f.read(b"oledata.mso")) == 234898
    assert (
        len(
            f.read(
                [
                    b"oledata.mso",
                    b"Firefox Setup Stub 43.0.1.exe",
                ]
            )
        )
        == 249336
    )


def test_read_stream():
    f = unpack(b"tests/files/bup_test.bup")
    s = f.read(b"efax_9057733019_pdf.zip", stream=True)
    assert len(s.read()) == 212663


def test_duplicate1():
    duplicates = []
    assert unpack(b"tests/files/garbage.bin", duplicates=duplicates).duplicate is False
    assert unpack(b"tests/files/garbage.bin", duplicates=duplicates).duplicate is True


def test_duplicate2():
    if ".7z" not in supported():
        return

    duplicates = []
    assert unpack(b"tests/files/7z_plain.7z", duplicates=duplicates).children[0].duplicate is False
    assert unpack(b"tests/files/7z_nested.7z", duplicates=duplicates).children[0].duplicate is True


def test_maxsize_7z():
    if ".7z" not in supported():
        return

    f = unpack(b"tests/files/1025mb.7z")
    assert f.unpacker == "7zfile"
    assert not f.children
    assert f.error == "files_too_large"


def test_maxsize_tar():
    f = unpack(b"tests/files/1025mb.tar.bz2")
    assert f.unpacker == "tarbz2file"
    assert not f.children
    assert f.error == "files_too_large"
