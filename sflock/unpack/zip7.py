# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from __future__ import absolute_import
from __future__ import print_function

import os
import tempfile

from sflock.abstracts import Unpacker
from sflock.exception import UnpackException


class ZipFile(Unpacker):
    name = "zipfile"
    exe = "/usr/bin/7z"
    exts = b".zip"
    magic = "Zip archive data"

    def supported(self):
        return True

    def handles(self):
        if super(ZipFile, self).handles():
            return True
        if self.f.stream.read(2) == b"PK":
            return True

    def unpack(self, password="infected", duplicates=None):
        dirpath = tempfile.mkdtemp()

        if not password:
            password = "infected"

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(b".zip")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", "-mmt=off", "-p%s" % password, "-o%s" % dirpath, filepath)

        dirlist = os.listdir(dirpath)
        if not ret and not dirlist:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, password=password)


class Zip7File(Unpacker):
    name = "7zfile"
    exe = "/usr/bin/7z"
    exts = b".7z", b".iso", b".udf", b".xz"
    # TODO Should we use "isoparser" (check PyPI) instead of 7z?
    magic = "7-zip archive", "ISO 9660", "UDF filesystem data", "XZ compressed data"

    def unpack(self, password="infected", duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(b".7z")
            temporary = True
        if not password:
            password = ""
        ret = self.zipjail(filepath, dirpath, "x", "-mmt=off", "-p{}".format(password), "-o{}".format(dirpath), filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class GzipFile(Unpacker):
    name = "gzipfile"
    exe = "/usr/bin/7z"
    exts = b".gzip", b".gz"
    magic = "gzip compressed data, was"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".7z")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", "-o%s" % dirpath, filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class LzhFile(Unpacker):
    name = "lzhfile"
    exe = "/usr/bin/7z"
    exts = b".lzh", b".lha"
    magic = "LHa ("

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".7z")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", "-o%s" % dirpath, filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class VHDFile(Unpacker):
    name = "vhdfile"
    exe = "/usr/bin/7z"
    exts = b".vhd", b".vhdx"
    magic = " Microsoft Disk Image"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".vhd")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", "-xr![SYSTEM]*", "-o%s" % dirpath, filepath)

        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class WimFile(Unpacker):
    name = "wimfile"
    exe = "/usr/bin/7z"
    exts = b".wim"
    magic = "Windows imaging (WIM) image"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".wim")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", "-o%s" % dirpath, filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class XZFile(Unpacker):
    name = "xzfile"
    exe = "/usr/bin/7z"
    exts = b".xz"
    magic = "XZ compressed data"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".7z")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", "-o%s" % dirpath, filepath)

        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class NSIS(Unpacker):
    name = "nsis"
    exe = "/usr/bin/7z"
    exts = b".exe"
    magic = "Nullsoft Installer self-extracting archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(b".7z")
            temporary = True
        ret = self.zipjail(filepath, dirpath, "x", "-mmt=off", "-o{}".format(dirpath), filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)
