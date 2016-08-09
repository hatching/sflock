# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import tarfile
from StringIO import StringIO

from sflock.abstracts import Unpacker, File

class Tarfile(Unpacker):
    name = "tarfile"
    author = ["Jurriaan Bremer", "Sander Ferdinand"]

    def __init__(self, f):
        super(Tarfile, self).__init__(f=f)
        self.signatures = {

        }

    def handles(self):
        if self.f.filepath:
            return tarfile.is_tarfile(self.f.filepath)
        else:
            return self._is_tarfile(contents=self.f.contents)

    def unpack(self, mode=None):
        if self.f.filepath:
            archive = self._openPath(self.f.filepath)
        else:
            archive = self._openStream(self.f.contents, mode=mode)

        for entry in archive:
            f = File(entry.path, archive.extractfile(entry).read())
            yield self.parse_item(f)

    @staticmethod
    def _is_tarfile(contents=None):
        from sflock.unpack.signatures import Signatures

        for k, v in Signatures.signatures.iteritems():
            if contents.startswith(k):
                return v

    def _openStream(self, contents, mode):
        from sflock.unpack.signatures import Signatures

        fileobj = StringIO(contents)
        if mode:
            return tarfile.open(mode=mode, fileobj=fileobj)

        for compression, info in Signatures.signatures.iteritems():
            if info["family"] != "tar":
                continue

            try:
                return tarfile.open(mode=info["mode"], fileobj=fileobj)
            except:
                pass

    @staticmethod
    def _openPath(filepath):
        try:
            archive = tarfile.TarFile.taropen(filepath)
        except tarfile.ReadError:
            try:
                archive = tarfile.TarFile.gzopen(filepath)
            except tarfile.ReadError:
                archive = tarfile.TarFile.bz2open(filepath)

        return archive