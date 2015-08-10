# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import UnitTest
from sflock.config import test_file
from sflock.unpack import Tarfile

class TarfileTestCase(UnitTest):
    def test_tar_plain(self):
        """Regular .tar file"""
        t = Tarfile(test_file("tar_plain.tar"))
        self.assertEqual(t.handles(), True)
        files = list(t.unpack())
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].filepath, "sflock.txt")
        self.assertEqual(files[0].contents, "sflock_plain_tar\n")
