# Copyright (C) 2015-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import bz2
import gzip
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
            archive = tarfile.open(mode=self.mode, fileobj=self.f.stream)
        except tarfile.ReadError as e:
            self.f.mode = "failed"
            self.f.error = e
            return []

        entries = []
        for entry in archive:
            # Ignore anything that's not a file for now.
            if not entry.isfile():
                continue

            entries.append(File(
                relapath=entry.path,
                contents=archive.extractfile(entry).read()
            ))

        return self.process(entries, duplicates)

class TargzFile(TarFile, Unpacker):
    name = "targzfile"
    mode = "r:gz"
    exts = ".tar.gz"

    def handles(self):
        if self.f.filename and self.f.filename.lower().endswith(self.exts):
            return True

        if not self.f.filesize:
            return False

        try:
            f = File(contents=gzip.GzipFile(fileobj=self.f.stream).read())
        except IOError:
            return False

        return self.magic in f.magic

class Tarbz2File(TarFile, Unpacker):
    name = "tarbz2file"
    mode = "r:bz2"
    exts = ".tar.bz2"

    def handles(self):
        if self.f.filename and self.f.filename.lower().endswith(self.exts):
            return True

        if not self.f.filesize:
            return False

        try:
            f = File(contents=bz2.decompress(self.f.contents))
        except IOError:
            return False

        return self.magic in f.magic
