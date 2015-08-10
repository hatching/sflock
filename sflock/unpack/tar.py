# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import tarfile

from sflock.abstracts import File, Unpacker

class Tarfile(Unpacker):
    name = "tarfile"
    author = ["Jurriaan Bremer"]

    def handles(self):
        return tarfile.is_tarfile(self.f.filepath)

    def unpack(self):
        try:
            archive = tarfile.TarFile.taropen(self.f.filepath)
        except tarfile.ReadError:
            try:
                archive = tarfile.TarFile.gzopen(self.f.filepath)
            except tarfile.ReadError:
                archive = tarfile.TarFile.bz2open(self.f.filepath)

        for entry in archive:
            yield File(entry.path, archive.extractfile(entry).read())
