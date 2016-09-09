# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker
from sflock.exception import UnpackException

class AceFile(Unpacker):
    name = "acefile"
    exe = "/usr/bin/unace"
    exts = ".ace"
    magic = "ACE archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()
        filepath = os.path.abspath(self.f.filepath)

        try:
            subprocess.check_call([
                self.zipjail, filepath, dirpath,
                self.exe, "x", filepath, dirpath + os.sep,
            ], stdin=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise UnpackException(e)

        return self.process_directory(dirpath, duplicates)
