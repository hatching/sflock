# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import os
import tempfile

from sflock.abstracts import File
from sflock.main import unpack

def test_temp_path():
    filepath = File(contents=b"foo").temp_path()
    assert open(filepath, "rb").read() == b"foo"

    filepath = File(stream=io.BytesIO(b"bar")).temp_path()
    assert open(filepath, "rb").read() == b"bar"

def test_stream():
    f = File(contents=b"foo1")
    assert f.filesize == 4
    assert f.stream.read() == b"foo1"

    f = File(stream=io.BytesIO(b"foo2"))
    assert f.filesize == 4
    assert f.stream.read() == b"foo2"

    fd, filepath = tempfile.mkstemp()
    os.write(fd, b"foobar")
    os.close(fd)

    f = File(stream=open(filepath, "rb"))
    assert f.filesize == 6
    assert f.stream.read() == b"foobar"
    assert f.sha256.startswith("c3ab8ff13720e8ad9047")

    f = File(stream=io.BytesIO(b"hello world"))
    assert f.stream.read() == b"hello world"
    assert f.stream.read(5) == b"hello"

    f = File(stream=io.BytesIO(b"hello world"))
    s = f.stream
    assert s.read(6) == b"hello "
    assert s.read() == b"world"
    assert f.sha256.startswith("b94d27b9934d3e08a52e52d7da7da")

def test_has_child():
    f = unpack("tests/files/doc_1.docx_")
    assert f.get_child("[Content_Types].xml") is not None
    assert f.get_child("docProps/app.xml") is not None
    assert f.get_child("docProps/.*\\.xml$", True) is not None
    assert f.get_child("docProps/.*\\.xmk", True) is None
