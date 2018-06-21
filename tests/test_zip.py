# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import os.path
import tempfile
import zipfile

from sflock.abstracts import File
from sflock.main import unpack, zipify
from sflock.unpack import ZipFile

def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))

class TestZipfile(object):
    def test_zip_plain(self):
        assert "Zip archive" in f(b"zip_plain.zip").magic
        z = ZipFile(f(b"zip_plain.zip"))
        assert z.handles() is True
        assert not z.f.selected
        assert z.f.preview is True
        files = list(z.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_plain_zip\n"
        assert files[0].password is None
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected
        assert files[0].preview is True

    def test_zip_encrypted(self):
        assert "Zip archive" in f(b"zip_encrypted.zip").magic
        z = ZipFile(f(b"zip_encrypted.zip"))
        assert z.handles() is True
        assert not z.f.selected
        assert z.f.preview is True
        files = list(z.unpack())
        assert len(files) == 1
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_encrypted_zip\n"
        assert files[0].password == b"infected"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_zip_encrypted2(self):
        assert "Zip archive" in f(b"zip_encrypted2.zip").magic
        z = ZipFile(f(b"zip_encrypted2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1
        assert files[0].mode == "failed"
        assert files[0].description == "Error decrypting file"
        assert files[0].magic is ""
        assert files[0].parentdirs == []
        assert not files[0].selected

        z = ZipFile(f(b"zip_encrypted2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack(b"sflock"))
        assert len(files) == 1
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_encrypted_zip\n"
        assert files[0].password == b"sflock"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

        z = ZipFile(f(b"zip_encrypted2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack([b"sflock"]))
        assert len(files) == 1
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_encrypted_zip\n"
        assert files[0].password == b"sflock"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_nested(self):
        assert "Zip archive" in f(b"zip_nested.zip").magic
        z = ZipFile(f(b"zip_nested.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1

        assert files[0].relapath == b"foo/bar.txt"
        assert files[0].parentdirs == [b"foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested2(self):
        assert "Zip archive" in f(b"zip_nested2.zip").magic
        z = ZipFile(f(b"zip_nested2.zip"))
        assert z.handles() is True
        assert not z.f.selected
        files = list(z.unpack())
        assert len(files) == 1

        assert files[0].relapath == b"deepfoo/foo/bar.txt"
        assert files[0].parentdirs == [b"deepfoo", b"foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_heuristics(self):
        t = unpack(b"tests/files/zip_plain.zip", filename=b"foo")
        assert t.unpacker == "zipfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/zip_nested.zip", filename=b"foo")
        assert t.unpacker == "zipfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/zip_nested2.zip", filename=b"foo")
        assert t.unpacker == "zipfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/zip_encrypted.zip", filename=b"foo")
        assert t.unpacker == "zipfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/zip_encrypted2.zip", filename=b"foo")
        assert t.unpacker == "zipfile"
        assert t.filename == b"foo"

    def test_garbage(self):
        t = ZipFile(f(b"garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert not t.unpack()
        assert t.f.mode == "failed"

    def test_garbage2(self):
        t = ZipFile(f(b"zip_garbage.zip"))
        assert t.handles() is True
        assert not t.f.selected
        assert t.f.preview is True
        files = t.unpack()
        assert len(files) == 1
        assert not files[0].children
        assert files[0].mode == "failed"

    def test_absolute_path(self):
        buf = io.BytesIO()
        z = zipfile.ZipFile(buf, "w")
        z.writestr("thisisfilename", "A"*1024)
        z.close()
        f = unpack(contents=buf.getvalue().replace(
            b"thisisfilename", b"/absolute/path"
        ))
        assert len(f.children) == 1
        assert f.children[0].filename == b"path"
        assert f.children[0].relapath == b"/absolute/path"
        assert f.children[0].relaname == b"absolute/path"
        assert f.children[0].contents == b"A"*1024
        assert f.read(b"/absolute/path") == b"A"*1024

    def test_docx1(self):
        t = ZipFile(f(b"doc_1.docx_"))
        assert t.handles()

    def test_partial(self):
        t = ZipFile(f(b"partial.zip"))
        assert t.handles()
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
