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
        "__sha256__": "fafd83b0a5f0f3ef5247fe9d196341b6a13e8c258b63921a59fef83ce711dc1d",
        "deepfoo": {
            "foo": {
                "bar.txt": {
                    "__sha256__": "a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447",
                },
            },
        },
    }

def test_astree2():
    f = unpack("tests/files/eml_tar_nested2.eml")
    assert f.astree() == {
        "__sha256__": "0c4a1d51e8f2ca75afaeb506bfec85e2b6195bcfe617081659bf1b758f05a953",
        "tar_nested2.tar": {
            "__sha256__": "42aa4bbacbbaee3404b4bf72d13e162a31d5a263ab5ab9e40171c28e4998b9fb",
            "deepfoo": {
                "foo": {
                    "bar.txt": {
                        "__sha256__": "a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447",
                    },
                },
            },
        },
    }
