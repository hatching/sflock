# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import UnitTest
from sflock.config import test_file
from sflock.unpack import Tarfile

class TarfileTestCase(UnitTest):
    def test_tar_plain(self):
        self.assertIn("POSIX tar", test_file("tar_plain.tar").magic)
        t = Tarfile(test_file("tar_plain.tar"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")
        self.assertEqual(files[0].magic, "ASCII text")

    def test_tar_plain2(self):
        self.assertIn("POSIX tar", test_file("tar_plain.tar").magic)
        t = Tarfile(test_file("tar_plain2.tar"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")
        self.assertEqual(files[0].magic, "ASCII text")
        self.assertEqual(files[1].filepath, "sflock2.txt")
        self.assertEqual(files[1].contents, "sflock_plain_tar2\n")
        self.assertEqual(files[1].magic, "ASCII text")

    def test_tar_plain2_gz(self):
        self.assertIn("gzip compr", test_file("tar_plain2.tar.gz").magic)
        t = Tarfile(test_file("tar_plain2.tar.gz"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")
        self.assertEqual(files[0].magic, "ASCII text")
        self.assertEqual(files[1].filepath, "sflock2.txt")
        self.assertEqual(files[1].contents, "sflock_plain_tar2\n")
        self.assertEqual(files[1].magic, "ASCII text")

    def test_tar_plain2_bz2(self):
        self.assertIn("bzip2 compr", test_file("tar_plain2.tar.bz2").magic)
        t = Tarfile(test_file("tar_plain2.tar.bz2"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")
        self.assertEqual(files[0].magic, "ASCII text")
        self.assertEqual(files[1].filepath, "sflock2.txt")
        self.assertEqual(files[1].contents, "sflock_plain_tar2\n")
        self.assertEqual(files[1].magic, "ASCII text")
