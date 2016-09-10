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
    magic = "7-zip archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if password:
            raise UnpackException(
                "Currently password-protected .7z files are not supported "
                "due to a ZipJail-related monitoring issue (namely, due to "
                "7z calling clone(2) when a password has been provided)."
            )

        try:
            subprocess.check_output([
                self.zipjail, self.f.filepath, dirpath,
                self.exe, "x", "-mmt=off", "-o%s" % dirpath, self.f.filepath,
            ])
        except subprocess.CalledProcessError as e:
            raise UnpackException(e)

        return self.process_directory(dirpath, duplicates)
