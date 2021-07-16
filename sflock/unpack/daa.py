# Copyright (C) 2019 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker
from sflock.misc import data_file


class DaaFile(Unpacker):
    name = "daafile"
    exts = b".daa"
    magic = "PowerISO Direct-Access-Archive"

    def __init__(self, *args, **kwargs):
        super(DaaFile, self).__init__(*args, **kwargs)
        self.exe = data_file(b"poweriso.elf")

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(".daa")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "extract", filepath, "/", "-od", dirpath)
        if temporary:
            os.unlink(filepath)

        if not ret:
            return []
        return self.process_directory(dirpath, duplicates)
