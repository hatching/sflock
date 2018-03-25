# Copyright (C) 2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker


class LzhFile(Unpacker):
    name = "lzhfile"
    exe = "/usr/bin/lha"
    exts = ".lzh"
    magic = "LHa ("

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(".lzh")
            temporary = True

        try:
            subprocess.check_call([
                self.zipjail, filepath, dirpath,
                self.exe, "xw={}".format(dirpath), filepath
            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            self.f.mode = "failed"
            self.f.error = e

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)
