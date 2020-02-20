# Copyright (C) 2016 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker

class AceFile(Unpacker):
    name = "acefile"
    exe = "/usr/bin/unace"
    exts = ".ace"
    magic = "ACE archive"

    def unpack(self, depth=0, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(".ace")
            temporary = True

        ret = self.zipjail(
            filepath, dirpath, "x", filepath, dirpath + os.sep
        )
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, depth)
