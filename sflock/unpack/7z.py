# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import subprocess
import tempfile

from sflock.abstracts import Unpacker
from sflock.exception import UnpackException

class Zip7File(Unpacker):
    name = "7zfile"
    exe = "/usr/bin/7z"
    exts = ".7z"

    def handles(self):
        return "7-zip archive" in self.f.magic

    def unpack(self, duplicates=None):
        dirpath = tempfile.mkdtemp()

        try:
            subprocess.check_call([
                self.zipjail, self.f.filepath, dirpath,
                self.exe, "x", "-mmt=off", "-o%s" % dirpath, self.f.filepath,
            ])
        except subprocess.CalledProcessError as e:
            raise UnpackException(e)

        return self.process_directory(dirpath, duplicates)
