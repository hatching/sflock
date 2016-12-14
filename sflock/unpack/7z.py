# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker
from sflock.exception import UnpackException

class Zip7File(Unpacker):
    name = "7zfile"
    exe = "/usr/bin/7z"
    exts = ".7z"
    magic = "7-zip archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if password:
            raise UnpackException(
                "Currently password-protected .7z files are not supported "
                "due to a ZipJail-related monitoring issue (namely, due to "
                "7z calling clone(2) when a password has been provided)."
            )

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".7z")
            temporary = True

        try:
            subprocess.check_output([
                self.zipjail, filepath, dirpath,
                self.exe, "x", "-mmt=off", "-o%s" % dirpath, filepath,
            ])
        except subprocess.CalledProcessError as e:
            self.f.mode = "failed"
            self.f.error = e

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)
