# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import UnitTest
from sflock.config import test_file
from sflock.unpack import Tarfile

class TarfileTestCase(UnitTest):
    def test_tar_plain(self):
        t = Tarfile(test_file("tar_plain.tar"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")

    def test_tar_plain2(self):
        t = Tarfile(test_file("tar_plain2.tar"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")
        self.assertEqual(files[1].filepath, "sflock2.txt")
        self.assertEqual(files[1].contents, "sflock_plain_tar2\n")

    def test_tar_plain2_gz(self):
        t = Tarfile(test_file("tar_plain2.tar.gz"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")
        self.assertEqual(files[1].filepath, "sflock2.txt")
        self.assertEqual(files[1].contents, "sflock_plain_tar2\n")

    def test_tar_plain2_bz2(self):
        t = Tarfile(test_file("tar_plain2.tar.bz2"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")
        self.assertEqual(files[1].filepath, "sflock2.txt")
        self.assertEqual(files[1].contents, "sflock_plain_tar2\n")
