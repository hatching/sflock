# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import tarfile
from StringIO import StringIO

from sflock.abstracts import Unpacker, File, Directory, Entries
from sflock.signatures import Signatures

class Tarfile(Unpacker):
    name = "tarfile"
    author = ["Jurriaan Bremer", "Sander Ferdinand"]

    def handles(self):
        if self.f.contents:
            return self._is_tarfile(contents=self.f.contents)
        else:
            return tarfile.is_tarfile(self.f.filepath)

    def unpack(self, mode=None):
        if self.f.contents:
            archive = self._open_stream(self.f.contents, mode=mode)
        else:
            archive = self._open_path(self.f.filepath)

        entries = Entries()
        for entry in archive:
            entries.children.append(File(entry.path, archive.extractfile(entry).read()))

            if "/" in entry.name:
                dirname = os.path.dirname(entry.name)
                if not dirname.endswith("/"):
                    dirname += "/"

                if not dirname or dirname == "/":
                    continue

                filepaths = [z.filepath for z in entries.children]
                if not dirname in filepaths:
                    entries.children.append(Directory(filepath=dirname))

        return self.parse_items(entries)

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
