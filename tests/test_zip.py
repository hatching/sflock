# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import os.path
import tempfile
import zipfile
import pytest

from sflock.abstracts import File
from sflock.errors import Errors
from sflock.exception import DecryptionFailedError
from sflock.main import unpack, zipify
from sflock.unpack import ZipFile, Zip7File

def f(filename):
    return File.from_path(os.path.join("tests", "files", filename))

class TestZipfile(object):
    def test_zip_plain(self):
        assert "Zip archive" in f("zip_plain.zip").magic
        z = ZipFile(f("zip_plain.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == b"sflock_plain_zip\n"
        assert files[0].password is None
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_zip_encrypted(self):
        assert "Zip archive" in f("zip_encrypted.zip").magic
        z = ZipFile(f("zip_encrypted.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == b"sflock_encrypted_zip\n"
        assert files[0].password == "infected"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_zip_encrypted2(self):
        assert "Zip archive" in f("zip_encrypted2.zip").magic
        z = ZipFile(f("zip_encrypted2.zip"))
        assert z.handles() is True
        assert not z.f.selected

        with pytest.raises(DecryptionFailedError) as e:
            z.unpack()
        assert e.value.state == Errors.DECRYPTION_FAILED

        z = ZipFile(f("zip_encrypted2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack(password="sflock"))
        assert len(files) == 1
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == b"sflock_encrypted_zip\n"
        assert files[0].password == "sflock"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

        z = ZipFile(f("zip_encrypted2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack(password=["sflock"]))
        assert len(files) == 1
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == b"sflock_encrypted_zip\n"
        assert files[0].password == "sflock"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_nested(self):
        assert "Zip archive" in f("zip_nested.zip").magic
        z = ZipFile(f("zip_nested.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1

        assert files[0].relapath == "foo/bar.txt"
        assert files[0].parentdirs == ["foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested2(self):
        assert "Zip archive" in f("zip_nested2.zip").magic
        z = ZipFile(f("zip_nested2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1

        assert files[0].relapath == "deepfoo/foo/bar.txt"
        assert files[0].parentdirs == ["deepfoo", "foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_heuristics(self):

        unpacker = "zipfile"
        if os.path.exists(Zip7File.exe):
            unpacker = "7zfile"

        t = unpack("tests/files/zip_plain.zip", filename="foo")
        assert t.unpacker == unpacker
        assert t.filename == "foo"

        t = unpack("tests/files/zip_nested.zip", filename="foo")
        assert t.unpacker == unpacker
        assert t.filename == "foo"

        t = unpack("tests/files/zip_nested2.zip", filename="foo")
        assert t.unpacker == unpacker
        assert t.filename == "foo"

        t = unpack("tests/files/zip_encrypted.zip", filename="foo")
        assert t.unpacker == unpacker
        assert t.filename == "foo"

        # No password provided - pass is sflock
        t = unpack("tests/files/zip_encrypted2.zip", filename="foo")
        assert t.mode == Errors.DECRYPTION_FAILED
        assert t.unpacker == unpacker
        assert t.filename == "foo"

    def test_garbage(self):
        t = ZipFile(f("garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert t.unpack() == []
        assert t.f.mode == Errors.INVALID_ARCHIVE

    def test_garbage2(self):
        t = ZipFile(f("zip_garbage.zip"))
        assert t.handles() is True
        assert not t.f.selected
        files = t.unpack()
        assert len(files) == 1
        assert not files[0].children
        assert files[0].mode is None

    def test_absolute_path(self):
        buf = io.BytesIO()
        z = zipfile.ZipFile(buf, "w")
        z.writestr("thisisfilename", "A"*1024)
        z.close()
        t = unpack(contents=buf.getvalue().replace(
            b"thisisfilename", b"/absolute/path"
        ))
        assert len(t.children) == 1
        assert t.children[0].filename == "path"
        assert t.children[0].relapath == "absolute/path"
        assert t.children[0].relaname == "absolute/path"
        assert t.children[0].contents == b"A"*1024
        assert t.read("absolute/path") == b"A"*1024

    def test_docx1(self):
        t = ZipFile(f("doc_1.docx_"))
        assert t.handles()

    def test_partial(self):
        # Has PK header, but is an invalid archive.
        t = ZipFile(f("partial.zip"))
        assert not t.handles()
        assert not t.unpack()

    def test_corrupt_directory(self):
        """Tests .zip files with an incorrectly named directory in it, namely
        by its filename missing the trailing slash."""
        buf = io.BytesIO()
        z = zipfile.ZipFile(buf, "w")
        z.writestr("foo", "")
        z.writestr("foo/bar", "baz")
        z.close()

        dirpath = tempfile.mkdtemp()

        # Test that zipfile.ZipFile().extractall() works on our zipped
        # version after unpacking. Zipception, basically.
        f = zipify(unpack(contents=buf.getvalue()))
        zipfile.ZipFile(io.BytesIO(f)).extractall(dirpath)

        filepath = os.path.join(dirpath, "foo", "bar")
        assert open(filepath, "rb").read() == b"baz"

    def test_whitespace_filename(self):
        """Tests .zip files with whitespace filenames in it, which can't be
        unpacked on Windows."""
        buf = io.BytesIO()
        z = zipfile.ZipFile(buf, "w")
        z.writestr(" ", "foo")
        z.writestr("  ", "bar")
        z.writestr("1.js", "baz")
        z.close()

        dirpath = tempfile.mkdtemp()

        # Test that zipfile.ZipFile().extractall() works on our zipped
        # version after unpacking. Zipception, basically.
        f = zipify(unpack(contents=buf.getvalue()))
        zipfile.ZipFile(io.BytesIO(f)).extractall(dirpath)

        assert len(os.listdir(dirpath)) == 1
        filepath = os.path.join(dirpath, "1.js")
        assert open(filepath, "rb").read() == b"baz"

    @pytest.mark.skip(reason="Zipjail command line requires user interaction")
    def test_invalid_characters(self):
        """Tests .zip files with invalid character filenames in it, which
        can't be unpacked on Windows."""
        buf = io.BytesIO()
        z = zipfile.ZipFile(buf, "w")
        z.writestr('foo"bar', "foo1")
        z.writestr("foo*bar", "foo2")
        z.writestr("foo<bar", "foo3")
        z.writestr("foo>bar", "foo4")
        z.writestr("foo?bar", "foo5")
        z.writestr("foo@bar", "foo5")
        z.writestr("1.js", "bar")
        z.close()

        dirpath = tempfile.mkdtemp()

        # Test that zipfile.ZipFile().extractall() works on our zipped
        # version after unpacking. Zipception, basically.
        f = zipify(unpack(contents=buf.getvalue()))
        zipfile.ZipFile(io.BytesIO(f)).extractall(dirpath)

        assert len(os.listdir(dirpath)) == 2
        filepath1 = os.path.join(dirpath, "foo@bar")
        filepath2 = os.path.join(dirpath, "1.js")
        assert open(filepath1, "rb").read() == b"foo5"
        assert open(filepath2, "rb").read() == b"bar"
