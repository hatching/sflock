# Copyright (C) 2016 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import shutil
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

        self.f.archive = True
        if self.f.filepath:
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(".ace")
            temporary = True

        symlink = None
        if not filepath.endswith(".ace"):
            symlink = tempfile.mkdtemp()
            new_filepath = os.path.join(symlink, "temp.ace")
            os.symlink(filepath, new_filepath)
            filepath = new_filepath

        ret = self.zipjail(
            filepath, dirpath, "x", filepath, dirpath + os.sep
        )

        if symlink:
            shutil.rmtree(symlink)

        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, depth)
