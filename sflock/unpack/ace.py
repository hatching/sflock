# Copyright (C) 2016 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from __future__ import absolute_import
from __future__ import print_function

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker


class AceFile(Unpacker):
    name = "acefile"
    exe = "/usr/bin/unace"
    exts = b".ace"
    magic = "ACE archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()
        original_path = self.f.filepath
        if self.f.filepath:
            if not self.f.filepath.endswith(b".ace"):
                os.rename(self.f.filepath, self.f.filepath + b".ace")
                self.f.filepath = self.f.filepath + b".ace"
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(b".ace")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", filepath, dirpath + os.sep)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        if original_path != self.f.filepath:
            os.rename(self.f.filepath, original_path)
            self.f.filepath = original_path

        return self.process_directory(dirpath, duplicates)
