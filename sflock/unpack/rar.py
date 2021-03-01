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

    def decrypt(self, password, archive, entry):
       return self.zipjail(
            archive, entry, "x", "-mt1", "-p%s" % (password or "-"),
            archive, entry
        )

    def unpack(self, depth=0, password=None, duplicates=None):
        self.f.archive = True
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        try:
            ret = self.bruteforce(password, filepath, dirpath)
        finally:
            if temporary:
                os.unlink(filepath)

        if not ret:
            return []

        return self.process_directory(dirpath, duplicates, depth, password)
