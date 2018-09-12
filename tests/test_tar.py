# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import TarFile, TargzFile, Tarbz2File

def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))

class TestTarFile(object):
    def test_tar_plain(self):
        assert "POSIX tar" in f(b"tar_plain.tar").magic
        t = TarFile(f(b"tar_plain.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_plain_tar\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected

    def test_tar_plain2(self):
        assert "POSIX tar" in f(b"tar_plain2.tar").magic
        t = TarFile(f(b"tar_plain2.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 2
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_plain_tar\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected
        assert files[1].relapath == b"sflock2.txt"
        assert files[1].contents == b"sflock_plain_tar2\n"
        assert files[1].magic == "ASCII text"
        assert files[1].parentdirs == []
        assert not files[1].selected

    def test_tar_plain2_gz(self):
        assert "gzip compr" in f(b"tar_plain2.tar.gz").magic
        t = TargzFile(f(b"tar_plain2.tar.gz"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 2
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_plain_tar\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected
        assert files[1].relapath == b"sflock2.txt"
        assert files[1].contents == b"sflock_plain_tar2\n"
        assert files[1].magic == "ASCII text"
        assert files[1].parentdirs == []
        assert not files[1].selected

    def test_tar_plain2_bz2(self):
        assert "bzip2 compr" in f(b"tar_plain2.tar.bz2").magic
        t = Tarbz2File(f(b"tar_plain2.tar.bz2"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        files = files[0].children
        assert len(files) == 2
        assert files[0].relapath == b"sflock.txt"
        assert files[0].contents == b"sflock_plain_tar\n"
        assert files[0].magic == "ASCII text"
        assert files[0].parentdirs == []
        assert not files[0].selected
        assert files[1].relapath == b"sflock2.txt"
        assert files[1].contents == b"sflock_plain_tar2\n"
        assert files[1].magic == "ASCII text"
        assert files[1].parentdirs == []
        assert not files[1].selected

    def test_nested_plain(self):
        assert "POSIX tar archive" in f(b"tar_nested.tar").magic
        t = TarFile(f(b"tar_nested.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == b"foo/bar.txt"
        assert files[0].parentdirs == [b"foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested_bzip2(self):
        assert "bzip2 compr" in f(b"tar_nested.tar.bz2").magic
        t = Tarbz2File(f(b"tar_nested.tar.bz2"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        files = files[0].children
        assert len(files) == 1
        assert files[0].relapath == b"foo/bar.txt"
        assert files[0].parentdirs == [b"foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested_gz(self):
        assert "gzip compr" in f(b"tar_nested.tar.gz").magic
        t = TargzFile(f(b"tar_nested.tar.gz"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == b"foo/bar.txt"
        assert files[0].parentdirs == [b"foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_nested2_plain(self):
        assert "POSIX tar archive" in f(b"tar_nested2.tar").magic
        t = TarFile(f(b"tar_nested2.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].relapath == b"deepfoo/foo/bar.txt"
        assert files[0].parentdirs == [b"deepfoo", b"foo"]
        assert files[0].contents == b"hello world\n"
        assert not files[0].password
        assert files[0].magic == "ASCII text"
        assert not files[0].selected

    def test_heuristics(self):
        t = unpack(b"tests/files/tar_plain.tar", filename=b"foo")
        assert t.unpacker == "tarfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/tar_plain2.tar", filename=b"foo")
        assert t.unpacker == "tarfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/tar_plain2.tar.gz", filename=b"foo")
        assert t.unpacker == "targzfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/tar_plain2.tar.bz2", filename=b"foo")
        assert t.unpacker == "tarbz2file"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/tar_nested.tar", filename=b"foo")
        assert t.unpacker == "tarfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/tar_nested.tar.gz", filename=b"foo")
        assert t.unpacker == "targzfile"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/tar_nested.tar.bz2", filename=b"foo")
        assert t.unpacker == "tarbz2file"
        assert t.filename == b"foo"

        t = unpack(b"tests/files/tar_nested2.tar", filename=b"foo")
        assert t.unpacker == "tarfile"
        assert t.filename == b"foo"

    def test_garbage(self):
        t = TarFile(f(b"garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert not t.unpack()
        assert t.f.mode == "failed"

    def test_garbage2(self):
        t = TarFile(f(b"tar_garbage.tar"))
        assert t.handles() is True
        assert not t.f.selected
        files = t.unpack()
        assert len(files) == 1
        assert not files[0].children
        assert files[0].mode == "failed"
