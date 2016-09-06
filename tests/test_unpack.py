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
    assert f.astree() == {
        "fafd83b0a5f0f3ef5247fe9d196341b6a13e8c258b63921a59fef83ce711dc1d": {
            "duplicate": False,
            "password": None,
            "finger": {
                "magic": "Zip archive data, at least v1.0 to extract",
                "magic_human": "Zip archive data (at least v1.0 to extract)",
                "mime": "application/zip",
                "mime_human": "zip",
            },
            "filename": "zip_nested2.zip",
            "filepath": "tests/files/zip_nested2.zip",
            "size": 496,
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
                                    "finger": {
                                          "magic": "ASCII text",
                                          "magic_human": "ASCII text",
                                          "mime": "text/plain",
                                          "mime_human": "plain",
                                    },
                                    "size": 12,
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
    assert f.astree() == {
        "0c4a1d51e8f2ca75afaeb506bfec85e2b6195bcfe617081659bf1b758f05a953": {
            "password": None,
            "finger": {
                "magic": "SMTP mail, ASCII text, with CRLF line terminators",
                "magic_human": "SMTP mail (ASCII text, with CRLF line terminators)",
                "mime": "message/rfc822",
                "mime_human": "rfc822",
            },
            "duplicate": False,
            "filename": "eml_tar_nested2.eml",
            "filepath": "tests/files/eml_tar_nested2.eml",
            "size": 15035,
            "password": None,
            "type": "container",
            "children": [
                {
                    "type": "container",
                    "password": None,
                    "finger": {
                        "magic": "POSIX tar archive (GNU)",
                        "magic_human": "POSIX tar archive (GNU)",
                        "mime": "application/x-tar",
                        "mime_human": "tar",
                    },
                    "duplicate": False,
                    "filename": u"tar_nested2.tar",
                    "filepath": u"tar_nested2.tar",
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
                                            "finger": {
                                                "magic": "ASCII text",
                                                "magic_human": "ASCII text",
                                                "mime": "text/plain",
                                                "mime_human": "plain",
                                            },
                                            "duplicate": False,
                                            "filename": "bar.txt",
                                            "filepath": "deepfoo/foo/bar.txt"
                                        },
                                    ],
                                },
                            ],
                        }
                    ],
                }
            ],

        },
    }
