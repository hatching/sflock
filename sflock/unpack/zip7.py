# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import tempfile
import zipfile

from sflock.abstracts import Unpacker

class Zip7File(Unpacker):
    name = "7zfile"
    exe = "/usr/bin/7z"
    exts = ".7z", ".iso", "zip"
    # TODO Should we use "isoparser" (check PyPI) instead of 7z?
    magic = "7-zip archive", "ISO 9660", "CDFV2 Encrypted", "Zip archive"
    priority = 1
    dependency = "p7zip-full"

    def handles(self):
        if super(Zip7File, self).handles():
            if self.f.stream.read(2) == b"PK":
                try:
                    zipfile.ZipFile(self.f.stream)
                    return True
                except (zipfile.BadZipFile, IOError):
                    return False

            return True

        return False

    def decrypt(self, password, archive, entry):
        if password:
            args = [f"-p{password}"]
        else:
            # Empty pass, otherwise it will prompt if there is a pass.
            args = ["-p"]

        return self.zipjail(
            archive, entry, "x", "-mmt=off", "-o%s" % entry, archive, *args
        )

    def unpack(self, depth=0, password=None, duplicates=None):
        self.f.archive = True
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(b".7z")
            temporary = True

        try:
            ret = self.bruteforce(password, filepath, dirpath)
        finally:
            if temporary:
                os.unlink(filepath)

        if not ret:
            return []

        return self.process_directory(dirpath, duplicates, depth)

class GzipFile(Unpacker):
    name = "gzipfile"
    exe = "/usr/bin/7z"
    exts = ".gzip"
    magic = "gzip compressed data, was"
    dependency = "p7zip-full"

    def unpack(self, depth=0, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".7z")
            temporary = True

        ret = self.zipjail(
            filepath, dirpath, "x", "-o%s" % dirpath, filepath
        )
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, depth)

class LzhFile(Unpacker):
    name = "lzhfile"
    exe = "/usr/bin/7z"
    exts = ".lzh", ".lha"
    magic = "LHa "
    dependency = "p7zip-full"

    def unpack(self, depth=0, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".7z")
            temporary = True

        ret = self.zipjail(
            filepath, dirpath, "x", "-o%s" % dirpath, filepath
        )
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, depth)

class VHDFile(Unpacker):
    name = "vhdfile"
    exe = "/usr/bin/7z"
    exts = ".vhd", ".vhdx"
    magic = " Microsoft Disk Image"
    dependency = "p7zip-full"

    def unpack(self, depth=0, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".vhd")
            temporary = True

        ret = self.zipjail(
            filepath, dirpath, "x", "-xr![SYSTEM]*", "-o%s" % dirpath, filepath
        )

        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, depth)
