# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import tarfile
from StringIO import StringIO

from sflock.abstracts import Unpacker, File
from sflock.signatures import Signatures

class Tarfile(Unpacker):
    name = "tarfile"
    author = ["Jurriaan Bremer", "Sander Ferdinand"]

    def handles(self):
        if self.f.filepath:
            return tarfile.is_tarfile(self.f.filepath)
        else:
            return self._is_tarfile(contents=self.f.contents)

    def unpack(self, mode=None):
        if self.f.filepath:
            archive = self._open_path(self.f.filepath)
        else:
            archive = self._open_stream(self.f.contents, mode=mode)

        for entry in archive:
            f = File(entry.path, archive.extractfile(entry).read())
            yield self.parse_item(f)

    def _is_tarfile(self, contents):
        for k, v in Signatures.signatures.items():
            if contents.startswith(k) and v["unpacker"] == "tarfile":
                return v

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
