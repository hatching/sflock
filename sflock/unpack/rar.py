# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import subprocess

from sflock.abstracts import File, Unpacker

class Rarfile(Unpacker):
    name = "rarfile"
    author = ["Jurriaan Bremer"]
    unrar = "/usr/bin/unrar"

    def handles(self):
        return "RAR archive" in self.f.magic

    def unpack(self):
        output = subprocess.check_output([self.unrar, "lb", self.f.filepath])
        for entry in output.split("\n"):
            # yield File(entry.path, archive.extractfile(entry).read())
            pass
