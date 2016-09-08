# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import tarfile
from StringIO import StringIO

from sflock.abstracts import Unpacker, File
from sflock.pick import picker
from sflock.signatures import Signatures

class TarFile(Unpacker):
    name = "tarfile"
    mode = None
    exts = ".tar"

    def supported(self):
        return True

    def handles(self):
        if picker(self.f.filepath) == self.name:
            return True

        if self.f.contents:
            return self._is_tarfile(contents=self.f.contents)
        else:
            return tarfile.is_tarfile(self.f.filepath)

    def unpack(self, password=None, duplicates=None):
        if self.f.contents:
            archive = self._open_stream(self.f.contents, mode=self.mode)
        else:
            archive = self._open_path(self.f.filepath)

        if not archive:
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

    def _is_tarfile(self, contents):
        for k, v in Signatures.signatures.items():
            if contents.startswith(k) and v["unpacker"] == self.name:
                return v
        return False

    def _open_stream(self, contents, mode):
        fileobj = StringIO(contents)

        if mode:
            return tarfile.open(mode=mode, fileobj=fileobj)

        for compression, info in Signatures.signatures.items():
            if info["family"] != "tar":
                continue

            try:
                return tarfile.open(mode=info["mode"], fileobj=fileobj)
            except:
                pass

    def _open_path(self, filepath):
        try:
            archive = tarfile.TarFile.taropen(filepath)
        except tarfile.ReadError:
            try:
                archive = tarfile.TarFile.gzopen(filepath)
            except tarfile.ReadError:
                archive = tarfile.TarFile.bz2open(filepath)

        return archive

class TargzFile(TarFile, Unpacker):
    name = "targzfile"
    mode = "r:gz"
    exts = ".tar.gz"

class Tarbz2File(TarFile, Unpacker):
    name = "tarbz2file"
    mode = "r:bz2"
    exts = ".tar.bz2"
