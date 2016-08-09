# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import tarfile
from StringIO import StringIO

from sflock.abstracts import Unpacker, File

class Tarfile(Unpacker):
    name = "tarfile"
    author = ["Jurriaan Bremer", "Sander Ferdinand"]

    def handles(self):
        if self.f.filepath:
            return tarfile.is_tarfile(self.f.filepath)
        else:
            return self._is_tarfile(contents=self.f.contents)

    def unpack(self):
        if self.f.filepath:
            archive = self._openPath(self.f.filepath)
        else:
            archive = self._openStream(self.f.contents)

        for entry in archive:
            f = File(entry.path, archive.extractfile(entry).read())
            yield self.parse_item(f)

    @staticmethod
    def _is_tarfile(contents=None):
        headers = {
            "tar": "\x75\x73\x74\x61\x72\x20\x20\x00",
            "bzip2": "\x42\x5A\x68",
            "gzip": "\x1F\x8B"
        }

        for k, v in headers.iteritems():
            if contents.startswith(v):
                return True

    @staticmethod
    def _openStream(contents):
        formats = {
            "tar": "r:*",
            "gzip": "r:gz",
            "bzip2": "r:bz2"
        }

        fileobj = StringIO(contents)

        for compression, mode in formats.iteritems():
            try:
                archive = tarfile.open(mode=mode, fileobj=fileobj)
                break
            except:
                pass

        return archive

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