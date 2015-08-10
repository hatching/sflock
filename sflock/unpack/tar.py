# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import tarfile

from sflock.abstracts import File, Unpacker

class Tarfile(Unpacker):
    name = "tarfile"
    author = ["Jurriaan Bremer"]

    def unpack(self):
        archive = tarfile.TarFile(self.filepath)
        for entry in archive:
            yield File(entry.path, archive.extractfile(entry).read())
