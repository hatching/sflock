# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker

class RarFile(Unpacker):
    name = "rarfile"
    exe = "/usr/bin/rar"
    exts = b".rar"
    magic = "RAR archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        ret = self.zipjail(
            filepath, dirpath, "x", "-mt1", b"-p%s" % (password or b"-"),
            filepath, dirpath
        )
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, password)
