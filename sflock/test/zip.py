# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import UnitTest
from sflock.config import test_file
from sflock.unpack import Zipfile

class ZipfileTestCase(UnitTest):
    def test_zip_plain(self):
        z = Zipfile(test_file("zip_plain.zip"))
        self.assertEqual(z.handles(), True)
        files = list(z.unpack())
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_zip\n")
        self.assertEqual(files[0].password, None)

    def test_zip_encrypted(self):
        z = Zipfile(test_file("zip_encrypted.zip"))
        self.assertEqual(z.handles(), True)
        files = list(z.unpack())
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_encrypted_zip\n")
        self.assertEqual(files[0].password, "infected")

    def test_zip_encrypted2(self):
        z = Zipfile(test_file("zip_encrypted2.zip"))
        self.assertEqual(z.handles(), True)
        files = list(z.unpack())
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].mode, "failed")
        self.assertEqual(files[0].description, "Error decrypting file")

        z = Zipfile(test_file("zip_encrypted2.zip"))
        self.assertEqual(z.handles(), True)
        files = list(z.unpack(password="sflock"))
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_encrypted_zip\n")
        self.assertEqual(files[0].password, "sflock")
