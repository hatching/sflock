# Copyright (C) 2017-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import tempfile

from sflock.abstracts import Unpacker


class CabFile(Unpacker):
    name = "cabfile"
    exe = "/usr/bin/cabextract"
    exts = ".cab"
    magic = "Microsoft Cabinet archive"
    dependency = "cabextract"

    def unpack(self, depth=0,  password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(".cab")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "-d%s" % dirpath, filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, depth)
