# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.main import unpack

def test_unpack1():
    f = unpack("tests/files/tar_plain.tar")
    assert len(f.children) == 1
    assert f.children[0].contents == "sflock_plain_tar\n"

def test_unpack2():
    f = unpack("tests/files/tar_nested.tar.bz2")
    assert len(f.children) == 1
    assert f.children[0].filepath == "foo/bar.txt"
    assert f.children[0].contents == "hello world\n"

def test_unpack3():
    f = unpack("tests/files/zip_nested2.zip")
    assert len(f.children) == 1
    assert f.children[0].filepath == "deepfoo/foo/bar.txt"
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
                                "filepath": "deepfoo/foo/bar.txt",
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
                "filepath": u"tar_nested2.tar",
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
                                        "filepath": "deepfoo/foo/bar.txt"
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
                "filepath": u"multipart.eml",
                "package": None,
                "selected": False,
                "password": None,
                "size": 17482,
                "type": "container",
                "children": [
                    {
                        "duplicate": False,
                        "filename": u"\u60e1\u610f\u8edf\u9ad4.doc",
                        "filepath": u"\u60e1\u610f\u8edf\u9ad4.doc",
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
                        "filepath": u"cuckoo.png",
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
                "duplicate": False,
                "filename": "att1",
                "filepath": "att1",
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
        "filepath": "tests/files/msg_invoice.msg",
        "filename": "msg_invoice.msg",
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
                "filepath": u"image003.emz",
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
                "filepath": u"image004.png",
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
                "filepath": u"oledata.mso",
                "package": "doc",
                "selected": True,
                "password": None,
                "size": 234898,
                "type": "container",
                "children": [
                    {
                        "duplicate": False,
                        "filename": "Firefox Setup Stub 43.0.1.exe",
                        "filepath": "Firefox Setup Stub 43.0.1.exe",
                        "package": "exe",
                        "selected": True,
                        "password": None,
                        "size": 249336,
                        "type": "file",
                        "children": [],
                    },
                ],
            },
        ],
    }
