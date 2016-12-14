# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker

class RarFile(Unpacker):
    name = "rarfile"
    exe = "/usr/bin/rar"
    exts = ".rar"
    magic = "RAR archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        try:
            subprocess.check_output([
                self.zipjail, filepath, dirpath,
                self.exe, "x", "-mt1", "-p%s" % (password or "-"),
                filepath, dirpath,
            ])
        except subprocess.CalledProcessError as e:
            self.f.mode = "failed"
            self.f.error = e

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, password)
