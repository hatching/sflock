# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import subprocess

from sflock.abstracts import Unpacker

class Rarfile(Unpacker):
    name = "rarfile"
    rar = "/usr/bin/rar"
    exts = ".rar"

    @staticmethod
    def supported():
        return os.path.exists(Rarfile.rar)

    def handles(self):
        return "RAR archive" in self.f.magic

    def unpack(self, mode=None):
        output = subprocess.check_output([self.unrar, "lb", self.f.filepath])
        for entry in output.split("\n"):
            # yield File(entry.path, archive.extractfile(entry).read())
            pass
