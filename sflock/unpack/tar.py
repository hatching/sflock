# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import tarfile

from sflock.abstracts import Unpacker, File

class TarFile(Unpacker):
    name = "tarfile"
    mode = "r:"
    exts = ".tar"
    magic = "POSIX tar archive"

    def supported(self):
        return True

    def unpack(self, password=None, duplicates=None):
        try:
            archive = tarfile.open(
                mode=self.mode, fileobj=io.BytesIO(self.f.contents)
            )
        except tarfile.ReadError:
            return self.process([], duplicates)

        entries = []
        for entry in archive:
            # Ignore anything that's not a file for now.
            if not entry.isfile():
                continue

            entries.append(
                File(entry.path, archive.extractfile(entry).read())
            )

        return self.process(entries, duplicates)

class TargzFile(TarFile, Unpacker):
    name = "targzfile"
    mode = "r:gz"
    exts = ".tar.gz"
    magic = "gzip compressed data"

class Tarbz2File(TarFile, Unpacker):
    name = "tarbz2file"
    mode = "r:bz2"
    exts = ".tar.bz2"
    magic = "bzip2 compressed data"
