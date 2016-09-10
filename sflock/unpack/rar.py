# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import subprocess
import tempfile

from sflock.abstracts import Unpacker
from sflock.exception import UnpackException

class RarFile(Unpacker):
    name = "rarfile"
    exe = "/usr/bin/rar"
    exts = ".rar"
    magic = "RAR archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        try:
            subprocess.check_output([
                self.zipjail, self.f.filepath, dirpath,
                self.exe, "x", "-mt1", "-p%s" % (password or "-"),
                self.f.filepath, dirpath,
            ])
        except subprocess.CalledProcessError as e:
            raise UnpackException(e)

        return self.process_directory(dirpath, duplicates, password)
