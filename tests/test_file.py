# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import os
import tempfile

from sflock.abstracts import File

def test_temp_path():
    filepath = File(contents="foo").temp_path()
    assert open(filepath, "rb").read() == "foo"

    filepath = File(stream=io.BytesIO("bar")).temp_path()
    assert open(filepath, "rb").read() == "bar"

def test_stream():
    f = File(contents="foo1")
    assert f.filesize == 4
    assert f.stream.read() == "foo1"

    f = File(stream=io.BytesIO("foo2"))
    assert f.filesize == 4
    assert f.stream.read() == "foo2"

    fd, filepath = tempfile.mkstemp()
    os.write(fd, "foobar")
    os.close(fd)

    f = File(stream=open(filepath, "rb"))
    assert f.filesize == 6
    assert f.stream.read() == "foobar"
    assert f.sha256.startswith("c3ab8ff13720e8ad9047")

    f = File(stream=io.BytesIO("hello world"))
    assert f.stream.read() == "hello world"
    assert f.stream.read(5) == "hello"

    f = File(stream=io.BytesIO("hello world"))
    s = f.stream
    assert s.read(6) == "hello "
    assert s.read() == "world"
    assert f.sha256.startswith("b94d27b9934d3e08a52e52d7da7da")
