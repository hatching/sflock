# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import tempfile

from sflock.main import unpack

def test_unpack1():
    f = unpack("tests/files/tar_plain.tar")
    assert len(f.children) == 1
    assert f.children[0].contents == "sflock_plain_tar\n"

def test_unpack2():
    f = unpack("tests/files/tar_nested.tar.bz2")
    assert len(f.children) == 1
    assert f.children[0].relapath == "foo/bar.txt"
    assert f.children[0].contents == "hello world\n"

def test_unpack3():
    f = unpack("tests/files/zip_nested2.zip")
    assert len(f.children) == 1
    assert f.children[0].relapath == "deepfoo/foo/bar.txt"
    assert f.children[0].contents == "hello world\n"

def test_unpack4():
    f = unpack("hoi.txt", "hello world")
    assert not f.children

def test_astree1():
    f = unpack("tests/files/zip_nested2.zip")
    assert f.astree(finger=False) == {
        "duplicate": False,
        "password": None,
        "filename": "zip_nested2.zip",
        "relapath": None,
        "filepath": "tests/files/zip_nested2.zip",
        "size": 496,
        "package": None,
        "selected": False,
        "type": "container",
        "children": [
            {
                "type": "directory",
                "filename": "deepfoo",
                "children": [
                    {
                        "type": "directory",
                        "filename": "foo",
                        "children": [
                            {
                                "filename": "bar.txt",
                                "relapath": "deepfoo/foo/bar.txt",
                                "filepath": None,
                                "duplicate": False,
                                "password": None,
                                "size": 12,
                                "package": None,
                                "selected": False,
                                "type": "file",
                                "children": [],
                            },
                        ],
                    },
                ],
            },
        ],
    }

def test_astree2():
    f = unpack("tests/files/eml_tar_nested2.eml")
    assert f.astree(finger=False) == {
        "password": None,
        "duplicate": False,
        "filename": "eml_tar_nested2.eml",
        "relapath": None,
        "filepath": "tests/files/eml_tar_nested2.eml",
        "size": 15035,
        "password": None,
        "package": None,
        "selected": False,
        "type": "container",
        "children": [
            {
                "type": "container",
                "password": None,
                "duplicate": False,
                "filename": u"tar_nested2.tar",
                "relapath": u"tar_nested2.tar",
                "filepath": None,
                "package": None,
                "selected": False,
                "size": 10240,
                "children": [
                    {
                        "type": "directory",
                        "filename": "deepfoo",
                        "children": [
                            {
                                "type": "directory",
                                "filename": "foo",
                                "children": [
                                    {
                                        "type": "file",
                                        "size": 12,
                                        "children": [],
                                        "password": None,
                                        "duplicate": False,
                                        "package": None,
                                        "selected": False,
                                        "filename": "bar.txt",
                                        "relapath": "deepfoo/foo/bar.txt",
                                        "filepath": None,
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    }

def test_astree3():
    f = unpack("tests/files/eml_nested_eml.eml")
    assert f.astree(finger=False) == {
        "duplicate": False,
        "filename": "eml_nested_eml.eml",
        "relapath": None,
        "filepath": "tests/files/eml_nested_eml.eml",
        "package": None,
        "selected": False,
        "password": None,
        "size": 24607,
        "type": "container",
        "children": [
            {
                "duplicate": False,
                "filename": u"multipart.eml",
                "relapath": u"multipart.eml",
                "filepath": None,
                "package": None,
                "selected": False,
                "password": None,
                "size": 17482,
                "type": "container",
                "children": [
                    {
                        "duplicate": False,
                        "filename": u"\u60e1\u610f\u8edf\u9ad4.doc",
                        "relapath": u"\u60e1\u610f\u8edf\u9ad4.doc",
                        "filepath": None,
                        "package": "doc",
                        "selected": True,
                        "password": None,
                        "size": 12,
                        "type": "file",
                        "children": [],
                    },
                    {
                        "duplicate": False,
                        "filename": u"cuckoo.png",
                        "relapath": u"cuckoo.png",
                        "filepath": None,
                        "package": None,
                        "selected": False,
                        "password": None,
                        "size": 11970,
                        "type": "file",
                        "children": [],
                    }
                ],
            },
            {
                "duplicate": True,
                "filename": "att1",
                "relapath": "att1",
                "filepath": None,
                "package": None,
                "selected": False,
                "password": None,
                "size": 12,
                "type": "file",
                "children": [],
            },
        ],
    }

def test_astree4():
    f = unpack("tests/files/msg_invoice.msg")
    assert f.astree(finger=False) == {
        "filename": "msg_invoice.msg",
        "relapath": None,
        "filepath": "tests/files/msg_invoice.msg",
        "size": 270848,
        "duplicate": False,
        "package": None,
        "selected": False,
        "password": None,
        "type": "container",
        "children": [
            {
                "duplicate": False,
                "filename": u"image003.emz",
                "relapath": u"image003.emz",
                "filepath": None,
                "package": None,
                "selected": False,
                "password": None,
                "size": 1137,
                "type": "file",
                "children": [],
            },
            {
                "duplicate": False,
                "filename": u"image004.png",
                "relapath": u"image004.png",
                "filepath": None,
                "package": None,
                "selected": False,
                "password": None,
                "size": 1132,
                "type": "file",
                "children": [],
            },
            {
                "duplicate": False,
                "filename": u"oledata.mso",
                "relapath": u"oledata.mso",
                "filepath": None,
                "package": "doc",
                "selected": True,
                "password": None,
                "size": 234898,
                "type": "container",
                "children": [
                    {
                        "duplicate": False,
                        "filename": "Firefox Setup Stub 43.0.1.exe",
                        "relapath": "Firefox Setup Stub 43.0.1.exe",
                        "filepath": None,
                        "package": "exe",
                        "selected": False,
                        "password": None,
                        "size": 249336,
                        "type": "file",
                        "children": [],
                    },
                ],
            },
        ],
    }

def test_extract1():
    unpack("tests/files/tar_plain.tar").extract("/tmp")
    assert open("/tmp/sflock.txt", "rb").read() == "sflock_plain_tar\n"

def test_extract2():
    unpack("tests/files/zip_nested2.zip").extract("/tmp")
    assert open("/tmp/bar.txt", "rb").read() == "hello world\n"

def test_extract3():
    dirpath = tempfile.mkdtemp()
    f = unpack("tests/files/bup_test.bup").children[0]

    f.extract(dirpath, "404.exe")
    assert not os.path.exists(
        os.path.join(dirpath, "404.exe")
    )
    assert not os.path.exists(
        os.path.join(dirpath, "efax_9057733019_pdf.scr")
    )

    f.extract(dirpath, "efax_9057733019_pdf.scr")
    filepath = os.path.join(dirpath, "efax_9057733019_pdf.scr")
    assert len(open(filepath, "rb").read()) == 377856
