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
        "fafd83b0a5f0f3ef5247fe9d196341b6a13e8c258b63921a59fef83ce711dc1d": {
            "duplicate": False,
            "password": None,
            "filename": "zip_nested2.zip",
            "filepath": "tests/files/zip_nested2.zip",
            "size": 496,
            "package": None,
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
                                    "type": "file",
                                    "children": [],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    }

def test_astree2():
    f = unpack("tests/files/eml_tar_nested2.eml")
    assert f.astree(finger=False) == {
        "0c4a1d51e8f2ca75afaeb506bfec85e2b6195bcfe617081659bf1b758f05a953": {
            "password": None,
            "duplicate": False,
            "filename": "eml_tar_nested2.eml",
            "filepath": "tests/files/eml_tar_nested2.eml",
            "size": 15035,
            "password": None,
            "package": None,
            "type": "container",
            "children": [
                {
                    "type": "container",
                    "password": None,
                    "duplicate": False,
                    "filename": u"tar_nested2.tar",
                    "filepath": u"tar_nested2.tar",
                    "package": None,
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
        },
    }

def test_astree3():
    f = unpack("tests/files/eml_nested_eml.eml")
    assert f.astree(finger=False) == {
        "78df974998868d10682fc3693bdfbbd61337923805b360394fae5e8371063f69": {
            "duplicate": False,
            "filename": "eml_nested_eml.eml",
            "filepath": "tests/files/eml_nested_eml.eml",
            "package": None,
            "password": None,
            "size": 24607,
            "type": "container",
            "children": [
                {
                    "duplicate": False,
                    "filename": u"multipart.eml",
                    "filepath": u"multipart.eml",
                    "package": None,
                    "password": None,
                    "size": 17482,
                    "type": "container",
                    "children": [
                        {
                            "duplicate": False,
                            "filename": u"\u60e1\u610f\u8edf\u9ad4.doc",
                            "filepath": u"\u60e1\u610f\u8edf\u9ad4.doc",
                            "package": "doc",
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
                    "password": None,
                    "size": 12,
                    "type": "file",
                    "children": [],
                },
            ],
        },
    }
