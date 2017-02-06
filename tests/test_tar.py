# Copyright (C) 2015-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import TarFile, TargzFile, Tarbz2File

def f(filename):
    return File.from_path("tests/files/%s" % filename)

class TestTarFile(object):
    def test_tar_plain(self):
        assert "POSIX tar" in f("tar_plain.tar").magic
        t = TarFile(f("tar_plain.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == "sflock_plain_tar\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_tar_plain2(self):
        assert "POSIX tar" in f("tar_plain2.tar").magic
        t = TarFile(f("tar_plain2.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 2
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == "sflock_plain_tar\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected
        assert files[1].relapath == "sflock2.txt"
        assert files[1].contents == "sflock_plain_tar2\n"
        assert files[1].magic == "ASCII text"
        assert files[1].parentdirs == []
        assert not files[1].selected

    def test_tar_plain2_gz(self):
        assert "gzip compr" in f("tar_plain2.tar.gz").magic
        t = TargzFile(f("tar_plain2.tar.gz"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 2
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == "sflock_plain_tar\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected
        assert files[1].relapath == "sflock2.txt"
        assert files[1].contents == "sflock_plain_tar2\n"
        assert files[1].magic == "ASCII text"
        assert files[1].parentdirs == []
        assert not files[1].selected

    def test_tar_plain2_bz2(self):
        assert "bzip2 compr" in f("tar_plain2.tar.bz2").magic
        t = Tarbz2File(f("tar_plain2.tar.bz2"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 2
        assert files[0].relapath == "sflock.txt"
        assert files[0].contents == "sflock_plain_tar\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected
        assert files[1].relapath == "sflock2.txt"
        assert files[1].contents == "sflock_plain_tar2\n"
        assert files[1].magic == "ASCII text"
        assert files[1].parentdirs == []
        assert not files[1].selected

    def test_nested_plain(self):
        assert "POSIX tar archive" in f("tar_nested.tar").magic
        t = TarFile(f("tar_nested.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "foo/bar.txt"
        assert files[0].parentdirs == ["foo"]
        assert files[0].contents == "hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested_bzip2(self):
        assert "bzip2 compr" in f("tar_nested.tar.bz2").magic
        t = Tarbz2File(f("tar_nested.tar.bz2"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "foo/bar.txt"
        assert files[0].parentdirs == ["foo"]
        assert files[0].contents == "hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested_gz(self):
        assert "gzip compr" in f("tar_nested.tar.gz").magic
        t = TargzFile(f("tar_nested.tar.gz"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "foo/bar.txt"
        assert files[0].parentdirs == ["foo"]
        assert files[0].contents == "hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested2_plain(self):
        assert "POSIX tar archive" in f("tar_nested2.tar").magic
        t = TarFile(f("tar_nested2.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == "deepfoo/foo/bar.txt"
        assert files[0].parentdirs == ["deepfoo", "foo"]
        assert files[0].contents == "hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_heuristics(self):
        t = unpack("tests/files/tar_plain.tar", filename="foo")
        assert t.unpacker == "tarfile"
        assert t.filename == "foo"

        t = unpack("tests/files/tar_plain2.tar", filename="foo")
        assert t.unpacker == "tarfile"
        assert t.filename == "foo"

        t = unpack("tests/files/tar_plain2.tar.gz", filename="foo")
        assert t.unpacker == "targzfile"
        assert t.filename == "foo"

        t = unpack("tests/files/tar_plain2.tar.bz2", filename="foo")
        assert t.unpacker == "tarbz2file"
        assert t.filename == "foo"

        t = unpack("tests/files/tar_nested.tar", filename="foo")
        assert t.unpacker == "tarfile"
        assert t.filename == "foo"

        t = unpack("tests/files/tar_nested.tar.gz", filename="foo")
        assert t.unpacker == "targzfile"
        assert t.filename == "foo"

        t = unpack("tests/files/tar_nested.tar.bz2", filename="foo")
        assert t.unpacker == "tarbz2file"
        assert t.filename == "foo"

        t = unpack("tests/files/tar_nested2.tar", filename="foo")
        assert t.unpacker == "tarfile"
        assert t.filename == "foo"

    def test_garbage(self):
        t = TarFile(f("garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert not t.unpack()
        assert t.f.mode == "failed"

    def test_garbage2(self):
        t = TarFile(f("tar_garbage.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = t.unpack()
        assert len(files) == 1
        assert not files[0].children
        assert files[0].mode == "failed"
