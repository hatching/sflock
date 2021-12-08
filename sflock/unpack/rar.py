# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import tempfile

from sflock.abstracts import Unpacker


class RarFile(Unpacker):
    name = "rarfile"
    exe = "/usr/bin/rar"
    exts = ".rar"
    magic = "RAR archive"
    dependency = "rar"

    def unpack(self, depth = 0, password: str = None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", "-mt1", "-p%s" % (password or "-"), filepath, dirpath)
        if not ret:
            return []

        return self.process_directory(dirpath, duplicates, depth, password)
