# Copyright (C) 2016-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import os.path
import tempfile
import zipfile
import pytest

from sflock.main import unpack, supported
from sflock.exception import MaxNestedError, UnpackException
from sflock.abstracts import File
from sflock.unpack.zip7 import Zip7File
from sflock.errors import Errors

def test_unpack_nested_max():
    with pytest.raises(MaxNestedError):
        unpack("tests/files/edge/data11.zip")

def test_unpack1():
    f = unpack("tests/files/tar_plain.tar")
    assert len(f.children) == 1
    assert f.children[0].contents == b"sflock_plain_tar\n"

def test_unpack2():
    f = unpack("tests/files/tar_nested.tar.bz2")
    assert len(f.children) == 1
    f = f.children[0]
    assert len(f.children) == 1
    assert f.children[0].relapath == "foo/bar.txt"
    assert f.children[0].relaname == "foo/bar.txt"
    assert f.children[0].contents == b"hello world\n"

def test_unpack3():
    f = unpack("tests/files/zip_nested2.zip")
    assert len(f.children) == 1
    assert f.children[0].relapath == "deepfoo/foo/bar.txt"
    assert f.children[0].relaname == "deepfoo/foo/bar.txt"
    assert f.children[0].contents == b"hello world\n"

def test_unpack4():
    f = unpack("hoi.txt", b"hello world")
    assert not f.children

def test_astree1():
    f = unpack("tests/files/zip_nested2.zip")
    assert f.astree(finger=False) == {
        "duplicate": False,
        "password": None,
        "filename": "zip_nested2.zip",
        "relapath": None,
        "relaname": None,
        "identified": True,
        "safelisted": False,
        "safelist_reason": "",
        "filepath": "tests/files/zip_nested2.zip",
        "extrpath": [],
        "size": 496,
        "extension": "zip",
        "platforms": [
            {"platform": "windows", "os_version": ""},
            {"platform": "darwin", "os_version": ""},
            {"platform": "linux", "os_version": ""},
            {"platform": "android", "os_version": ""},
            {"platform": "ios", "os_version": ""}
        ],
        "dependency": "unarchive",
        "dependency_version": "",
        "human_type": "ZIP file",
        "selected": False,
        "selectable": False,
        'md5': '3abc01796865fe807be0f41ec65a213e',
        'sha1': '7fbdb77602fd1070850bd5d743a53c07ac066b59',
        'sha256': 'fafd83b0a5f0f3ef5247fe9d196341b6a13e8c258b63921a59fef83ce711dc1d',
        "error": None,
        "type": "container",
        "children": [{
            "type": "directory",
            "filename": "deepfoo",
            "children": [{
                "type": "directory",
                "filename": "foo",
                "children": [{
                    "filename": "bar.txt",
                    "relapath": "deepfoo/foo/bar.txt",
                    "relaname": "deepfoo/foo/bar.txt",
                    "filepath": None,
                    "extrpath": [
                        "deepfoo/foo/bar.txt",
                    ],
                    "duplicate": False,
                    "password": None,
                    "identified": True,
                    "size": 12,
                    "extension": "txt",
                    "platforms": [
                        {"platform": "windows", "os_version": ""},
                        {"platform": "darwin", "os_version": ""},
                        {"platform": "linux", "os_version": ""},
                        {"platform": "android", "os_version": ""},
                        {"platform": "ios", "os_version": ""}
                    ],
                    "dependency": "",
                    "dependency_version": "",
                    "safelisted": False,
                    "safelist_reason": "",
                    "human_type": "Text",
                    "selected": False,
                    "selectable": False,
                    'md5': '6f5902ac237024bdd0c176cb93063dc4',
                    'sha1': '22596363b3de40b06f981fb85d82312e8c0ed511',
                    'sha256': 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447',
                    "error": None,
                    "type": "file",
                    "children": [],
                }],
            }],
        }],
    }

def test_astree2():
    f = unpack("tests/files/eml_tar_nested2.eml")
    assert f.astree(finger=False) == {
        "password": None,
        "duplicate": False,
        "filename": "eml_tar_nested2.eml",
        "relapath": None,
        "relaname": None,
        "filepath": "tests/files/eml_tar_nested2.eml",
        "extrpath": [],
        "size": 15035,
        "identified": True,
        "extension": "email",
        "platforms": [
            {"platform": "windows", "os_version": ""}
        ],
        "dependency": "",
        "dependency_version": "",
        "human_type": "Email file",
        "safelisted": False,
        "safelist_reason": "",
        "selected": False,
        "selectable": False,
        'md5': 'ded1a5de62d0882f41613b00d5be02f3',
        'sha1': '8bbfc981546ef851f164a6aec91e92781674091a',
        'sha256': '0c4a1d51e8f2ca75afaeb506bfec85e2b6195bcfe617081659bf1b758f05a953',
        "error": None,
        "type": "container",
        "children": [{
            "type": "container",
            "password": None,
            "duplicate": False,
            "identified": True,
            "filename": "tar_nested2.tar",
            "relapath": "tar_nested2.tar",
            "relaname": "tar_nested2.tar",
            "filepath": None,
            "extrpath": [
                "tar_nested2.tar",
            ],
            "extension": "tar",
            "platforms": [
                {"platform": "linux", "os_version": ""}
            ],
            "safelisted": False,
            "safelist_reason": "",
            "dependency": "",
            "dependency_version": "",
            "human_type": "Consolidated Unix File Archive",
            "selected": False,
            "selectable": False,
            'md5': '408330e5b4ab14362ecf0e9f7fb546fc',
            'sha1': '52be5d3a95baf329d2aa9ffeb079124731fb2c1b',
            'sha256': '42aa4bbacbbaee3404b4bf72d13e162a31d5a263ab5ab9e40171c28e4998b9fb',
            "error": None,
            "size": 10240,
            "children": [{
                "type": "directory",
                "filename": "deepfoo",
                "children": [{
                    "type": "directory",
                    "filename": "foo",
                    "children": [{
                        "type": "file",
                        "size": 12,
                        "children": [],
                        "password": None,
                        "duplicate": False,
                        "identified": True,
                        "extension": "txt",
                        "platforms":[
                            {"platform": "windows", "os_version": ""},
                            {"platform": "darwin", "os_version": ""},
                            {"platform": "linux", "os_version": ""},
                            {"platform": "android", "os_version": ""},
                            {"platform": "ios", "os_version": ""}
                        ],
                        "dependency": "",
                        "dependency_version": "",
                        "human_type": "Text",
                        "safelisted": False,
                        "safelist_reason": "",
                        "selected": False,
                        "selectable": False,
                        'md5': '6f5902ac237024bdd0c176cb93063dc4',
                        'sha1': '22596363b3de40b06f981fb85d82312e8c0ed511',
                        'sha256': 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447',
                        "error": None,
                        "filename": "bar.txt",
                        "relapath": "deepfoo/foo/bar.txt",
                        "relaname": "deepfoo/foo/bar.txt",
                        "filepath": None,
                        "extrpath": [
                            "tar_nested2.tar",
                            "deepfoo/foo/bar.txt",
                        ],
                    }],
                }],
            }],
        }],
    }

def test_astree3():
    f = unpack("tests/files/eml_nested_eml.eml")
    assert f.astree(finger=False) == {
        "extension": "mht",
        "platforms": [
            {"platform": "windows", "os_version": ""},
            {"platform": "darwin", "os_version": ""},
            {"platform": "linux", "os_version": ""},
            {"platform": "android", "os_version": ""},
            {"platform": "ios", "os_version": ""}
        ],
        "dependency": "",
        "dependency_version": "",
        "human_type": "Mht file",
        "duplicate": False,
        "filename": "eml_nested_eml.eml",
        "relapath": None,
        "relaname": None,
        "filepath": "tests/files/eml_nested_eml.eml",
        "extrpath": [],
        "selected": True,
        "selectable": True,
        "safelisted": False,
        "safelist_reason": "",
        'md5': '8199175d177670279f05eeb890f4092a',
        'sha1': 'f35de26d11ac2904fbdee9bab8ce502526ccc58e',
        'sha256': '78df974998868d10682fc3693bdfbbd61337923805b360394fae5e8371063f69',
        "password": None,
        "identified": True,
        "size": 24607,
        "error": None,
        "type": "container",
        "children": [{
            "extension": "mht",
            "platforms": [
                {"platform": "windows", "os_version": ""},
                {"platform": "darwin", "os_version": ""},
                {"platform": "linux", "os_version": ""},
                {"platform": "android", "os_version": ""},
                {"platform": "ios", "os_version": ""}
            ],
            "dependency": "",
            "dependency_version": "",
            "safelisted": False,
            "safelist_reason": "",
            "human_type": "Mht file",
            "duplicate": False,
            "filename": "multipart.eml",
            "relapath": "multipart.eml",
            "relaname": "multipart.eml",
            "identified": True,
            "filepath": None,
            "extrpath": [
                "multipart.eml",
            ],
            "selected": True,
            "selectable": True,
            'md5': 'c73223b697d256cc3ef6d8d38349d72e',
            'sha1': '144422a989ebdcfffb32e9a075de8655ca632408',
            'sha256': 'b9079482871148f3c2201260a207c3a6fc02508ec56a7689e3f5771f1794d3aa',
            "password": None,
            "size": 17482,
            "error": None,
            "type": "container",
            "children": [{
                "extension": "txt",
                "platforms": [
                    {"platform": "windows", "os_version": ""},
                    {"platform": "darwin", "os_version": ""},
                    {"platform": "linux", "os_version": ""},
                    {"platform": "android", "os_version": ""},
                    {"platform": "ios", "os_version": ""}
                ],
                "safelisted": False,
                "safelist_reason": "",
                "dependency": "",
                "dependency_version": "",
                "human_type": "Text",
                "duplicate": False,
                "filename": u"\u60e1\u610f\u8edf\u9ad4.doc",
                "relapath": u"\u60e1\u610f\u8edf\u9ad4.doc",
                "relaname": u"\u60e1\u610f\u8edf\u9ad4.doc",
                "identified": True,
                "filepath": None,
                "extrpath": [
                    "multipart.eml",
                    u"\u60e1\u610f\u8edf\u9ad4.doc",
                ],
                "selected": False,
                "selectable": False,
                'md5': '07effd09e085b24c2de0de291e06c449',
                'sha1': '2f543e2ebc872906fe79ed0fe7cff1bb7e25ef0d',
                'sha256': '7aa4f32dd8dde9f69c1ef5176f8ed9f2964563721edd1b1647cab377b1f60884',
                "password": None,
                "size": 12,
                "error": None,
                "type": "file",
                "children": [],
            }, {
                "extension": "png",
                "platforms": [
                    {"platform": "windows", "os_version": ""},
                    {"platform": "darwin", "os_version": ""},
                    {"platform": "linux", "os_version": ""},
                    {"platform": "android", "os_version": ""},
                    {"platform": "ios", "os_version": ""}
                ],
                "safelisted": False,
                "safelist_reason": "",
                "dependency": "",
                "dependency_version": "",
                "human_type": "Portable Network Graphic",
                "duplicate": False,
                "filename": "cuckoo.png",
                "relapath": "cuckoo.png",
                "identified": True,
                "relaname": "cuckoo.png",
                "filepath": None,
                "extrpath": [
                    "multipart.eml",
                    "cuckoo.png",
                ],
                "selected": False,
                "selectable": False,
                'md5': '960884921427867f498968e7e463b580',
                'sha1': '0640f27337118ce1876a6b9f8299f60a729506a8',
                'sha256': 'c89aaba3a40660dcb0fec476f97cf5b45b31da94ea272f5a242f03db743ebf27',
                "password": None,
                "size": 11970,
                "error": None,
                "type": "file",
                "children": [],
            }],
        }, {
            "duplicate": True,
            "filename": "att1",
            "relapath": "att1",
            "relaname": "att1",
            "identified": True,
            "filepath": None,
            "extrpath": [
                "att1",
            ],
            "extension": "txt",
            "platforms": [
                {"platform": "windows", "os_version": ""},
                {"platform": "darwin", "os_version": ""},
                {"platform": "linux", "os_version": ""},
                {"platform": "android", "os_version": ""},
                {"platform": "ios", "os_version": ""}
            ],
            "safelisted": False,
            "safelist_reason": "",
            "dependency": "",
            "dependency_version": "",
            "human_type": "Text",
            "selected": False,
            "selectable": False,
            'md5': '07effd09e085b24c2de0de291e06c449',
            'sha1': '2f543e2ebc872906fe79ed0fe7cff1bb7e25ef0d',
            'sha256': '7aa4f32dd8dde9f69c1ef5176f8ed9f2964563721edd1b1647cab377b1f60884',
            "password": None,
            "size": 12,
            "error": None,
            "type": "file",
            "children": [],
        }],
    }

def test_astree4():
    f = unpack("tests/files/msg_invoice.msg")
    assert f.astree(finger=False) == {
        "filename": "msg_invoice.msg",
        "relapath": None,
        "relaname": None,
        "filepath": "tests/files/msg_invoice.msg",
        "human_type": "Microsoft outlook message",
        "extension": "msg",
        "extrpath": [],
        "size": 270848,
        "identified": True,
        "duplicate": False,
        'sha1': 'c5c1d805d8d2bed2143f410e04c57da41024777e',
        'sha256': 'ec226fcd63e0803deb1b99622c774247fec651b2645929341ebc837b9ed7eeb5',
        'md5': 'bbff75488a3dcc01c081c35dd3589f8e',
        "platforms": [
            {"platform": "windows", "os_version": ""},
            {"platform": "darwin", "os_version": ""},
            {"platform": "linux", "os_version": ""},
            {"platform": "android", "os_version": ""},
            {"platform": "ios", "os_version": ""}
        ],
        "selected": False,
        "selectable": False,
        "password": None,
        "error": None,
        "safelisted": False,
        "safelist_reason": "",
        "dependency": "microsoft_outlook",
        "dependency_version": "",
        "type": "container",
        "children": [{
            "safelisted": False,
            "safelist_reason": "",
            "dependency": "unarchive",
            "dependency_version": "",
            "duplicate": False,
            "filename": "image003.emz",
            "relapath": "image003.emz",
            "relaname": "image003.emz",
            "filepath": None,
            "extrpath": [
                "image003.emz",
            ],
            "extension": "gz",
            "human_type": "GZIP compressed file",
            "platforms": [
                {"platform": "linux", "os_version": ""}
            ],
            "selected": False,
            "selectable": False,
            'sha1': 'f4a6adc6fb59b49a07660e3c2a577b210ea99404',
            'sha256': 'f05ae6aeba0d5145a1f3e73bdd20cc0d9f2069dc9a2d7c954ce0cedd457f3b2b',
            'md5': '31929aa58698beec4d4d1684e725df59',
            "password": None,
            "identified": True,
            "size": 1137,
            "error": "invalid header",
            "type": "file",
            "children": [],
        }, {
            "duplicate": False,
            "safelisted": False,
            "safelist_reason": "",
            "dependency": "",
            "dependency_version": "",
            "extension": "png",
            "human_type": "Portable Network Graphic",
            "filename": "image004.png",
            "relapath": "image004.png",
            "relaname": "image004.png",
            "filepath": None,
            "identified": True,
            "extrpath": [
                "image004.png",
            ],
            "platforms": [
                {"platform": "windows", "os_version": ""},
                {"platform": "darwin", "os_version": ""},
                {"platform": "linux", "os_version": ""},
                {"platform": "android", "os_version": ""},
                {"platform": "ios", "os_version": ""}
            ],
            "selected": False,
            "selectable": False,
            'sha1': '311d7be3594ffc44360299fa88494f5c98008b59',
            'sha256': '0600e455fb5996dee84978031fde9a5a3afe5563dfcbf9e5b0400b7140f19c7c',
            'md5': '65fc3ca9139761011dbc54f93ddbb9c1',
            "password": None,
            "size": 1132,
            "error": None,
            "type": "file",
            "children": [],
        }, {
            "duplicate": False,
            "human_type": "Random bytes/Memory dump",
            "extension": "",
            "filename": "oledata.mso",
            "relapath": "oledata.mso",
            "relaname": "oledata.mso",
            "filepath": None,
            "identified": True,
            "extrpath": [
                "oledata.mso",
            ],
            "platforms": [],
            "safelisted": False,
            "safelist_reason": "",
            "dependency": "",
            "dependency_version": "",
            "selected": False,
            "selectable": False,
            'md5': '7255ad3d87b8c487921804fc9e7f1beb',
            'sha1': '1dcb06a8f8c6b381757c7eedb22a5203306627ab',
            'sha256': '42e0d00b6cdeeab79f8a9c5c00acc2d33c3ece490cb9bfb49733f87ffa4a73e0',
            "password": None,
            "size": 234898,
            "error": None,
            "type": "container",
            "children": [{
                "safelisted": False,
                "safelist_reason": "",
                "dependency": "",
                "dependency_version": "",
                "extension": "exe",
                "duplicate": False,
                "filename": "Firefox Setup Stub 43.0.1.exe",
                "relapath": "Firefox Setup Stub 43.0.1.exe",
                "relaname": "Firefox Setup Stub 43.0.1.exe",
                "filepath": None,
                "identified": True,
                "human_type": "Exe file",
                "platforms": [
                    {"platform": "windows", "os_version": ""},
                ],
                "extrpath": [
                    "oledata.mso",
                    "Firefox Setup Stub 43.0.1.exe",
                ],
                "platforms": [
                    {"platform": "windows", "os_version": ""},
                ],
                "selected": True,
                "selectable": True,
                'md5': 'c8cd8eb88f1848cf456725d67baaaa35',
                'sha1': '2b5f83cfdd2384782ae7b530e795a6d79a05336f',
                'sha256': 'e15ca271ba7eb8714a172f193096bfdb9b562ad53eb88379004792182c7cfa1b',
                "password": None,
                "size": 249336,
                "error": None,
                "type": "file",
                "children": [],
            }],
        }],
    }

def test_astree_sanitize():
    f = unpack("tests/files/msg_invoice.msg")
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
    dirpath = tempfile.gettempdir()
    tmpdir = tempfile.gettempdir()
    unpack("tests/files/tar_plain.tar").extract(dirpath)
    filepath = os.path.join(tmpdir, "sflock.txt")
    assert open(filepath, "rb").read() == b"sflock_plain_tar\n"

def test_extract2():
    tmpdir = tempfile.gettempdir()
    unpack("tests/files/zip_nested2.zip").extract(tmpdir)
    filepath = os.path.join(tmpdir, "bar.txt")
    assert open(filepath, "rb").read() == b"hello world\n"

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

def test_extract4_nopreserve():
    buf = io.BytesIO()
    z = zipfile.ZipFile(buf, "w")
    z.writestr("thisisfilename", "B"*1024)
    z.close()
    f = unpack(contents=buf.getvalue().replace(
        b"thisisfilename", b"/absolute/path"
    ))
    dirpath = tempfile.mkdtemp(prefix="sfl")
    f.extract(dirpath, preserve=True)

    filepath = os.path.join(dirpath, "absolute", "path")
    assert os.path.exists(filepath)
    assert open(filepath, "rb").read() == b"B"*1024

def test_extract5_relative_no_spf():
    buf = io.BytesIO()
    z = zipfile.ZipFile(buf, "w")
    z.writestr("foobarfilename", "A"*1024)
    z.writestr("thisisfilename", "B"*1024)
    z.close()
    f = unpack(contents=buf.getvalue().replace(
        b"thisisfilename", b"/../../../rela"
    ))
    dirpath = tempfile.mkdtemp(prefix="sfl")

    f.extract(dirpath, preserve=True)
    assert len(os.listdir(dirpath)) == 2

    filepath = os.path.join(dirpath, "foobarfilename")
    assert open(filepath, "rb").read() == b"A"*1024

def test_extract5_relative_spf():
    """
    This test demonstrates the 7z unpacking using the -spf flag

    This flag enables 7z to enter an unsafe mode, it will try to write
    files to a relative directory.

    In this test Zipjail will catch the directory_traversal error
    """
    buf = io.BytesIO()
    z = zipfile.ZipFile(buf, "w")
    z.writestr("foobarfilename", "A"*1024)
    z.writestr("thisisfilename", "B"*1024)
    z.close()

    contents = buf.getvalue().replace(
        b"thisisfilename", b"/../../../rela"
    )
    f = File(None, contents, filename=None)
    filepath = f.temp_path(b".7z")
    dirpath = tempfile.mkdtemp()
    u = Zip7File(f)
    u.name = "7zfile"
    args = ["-spf"]

    with pytest.raises(UnpackException) as e:
        u.zipjail(
            filepath, dirpath, "x", "-mmt=off", "-o%s" % dirpath, filepath,
            *args
        )
    assert e.value.state == Errors.CANCELLED_DIR_TRAVERSAL
    assert len(os.listdir(dirpath)) == 1
    filepath = os.path.join(dirpath, "foobarfilename")
    assert open(filepath, "rb").read() == b"A"*1024

def test_duplicate():
    duplicates = []
    f1 = unpack("tests/files/tar_plain.tar", duplicates=duplicates)
    f2 = unpack("tests/files/tar_plain.tar", duplicates=duplicates)
    assert f1.children[0].duplicate is False
    assert f2.children[0].duplicate is True

def test_read1():
    f = unpack("tests/files/bup_test.bup")
    assert len(f.read("efax_9057733019_pdf.zip")) == 212663
    assert len(f.read([
        "efax_9057733019_pdf.zip", "efax_9057733019_pdf.scr",
    ])) == 377856

def test_read2():
    f = unpack("tests/files/msg_invoice.msg")
    assert len(f.read("oledata.mso")) == 234898
    assert len(f.read([
        "oledata.mso", "Firefox Setup Stub 43.0.1.exe",
    ])) == 249336

def test_read_stream():
    f = unpack("tests/files/bup_test.bup")
    s = f.read("efax_9057733019_pdf.zip", stream=True)
    assert len(s.read()) == 212663

def test_duplicate1():
    duplicates = []
    assert unpack(
        "tests/files/garbage.bin", duplicates=duplicates
    ).duplicate is False
    assert unpack(
        "tests/files/garbage.bin", duplicates=duplicates
    ).duplicate is True

def test_duplicate2():
    if ".7z" not in supported():
        return

    duplicates = []
    assert unpack(
        "tests/files/7z_plain.7z", duplicates=duplicates
    ).children[0].duplicate is False
    assert unpack(
        "tests/files/7z_nested.7z", duplicates=duplicates
    ).children[0].duplicate is True

def test_maxsize_7z():
    if ".7z" not in supported():
        return

    f = unpack("tests/files/1025mb.7z")
    assert f.unpacker == "7zfile"
    assert not f.children
    assert f.mode == Errors.TOTAL_TOO_LARGE

def test_maxsize_tar():
    f = unpack("tests/files/1025mb.tar.bz2")
    assert f.unpacker == "tarbz2file"
    assert not f.children
    assert f.mode == Errors.TOTAL_TOO_LARGE

def test_maxsize_zip():
    f = unpack("tests/files/1025mb.zip")
    assert f.unpacker in ("zipfile", "7zfile")
    assert not f.children
    assert f.mode == Errors.TOTAL_TOO_LARGE

