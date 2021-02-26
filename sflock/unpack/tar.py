# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import bz2
import gzip
import os
import tarfile
import tempfile

from sflock.abstracts import Unpacker, File
from sflock.config import MAX_TOTAL_SIZE
from sflock.errors import Errors

class TarFile(Unpacker):
    name = "tarfile"
    mode = "r:"
    exts = ".tar"
    magic = "POSIX tar archive"

    def supported(self):
        return True

    def unpack(self, depth=0, password=None, duplicates=None):
        self.f.archive = True
        try:
            archive = tarfile.open(mode=self.mode, fileobj=self.f.stream)
        except tarfile.ReadError as e:
            self.f.set_error(Errors.INVALID_ARCHIVE, str(e))
            return []

        entries, total_size = [], 0
        for entry in archive:
            # Ignore anything that's not a file for now.
            if not entry.isfile() or entry.size < 0:
                continue

            # TODO Improve this. Also take precedence for native decompression
            # utilities over the Python implementation in the future.
            total_size += entry.size
            if total_size >= MAX_TOTAL_SIZE:
                self.f.set_error(
                    Errors.TOTAL_TOO_LARGE,
                    f"Unpacked archive size exceeds: {MAX_TOTAL_SIZE}"
                )
                return []

            entries.append(File(
                relapath=entry.path,
                contents=archive.extractfile(entry).read()
            ))

        return self.process(entries, duplicates, depth)

class TargzFile(TarFile, Unpacker):
    name = "targzfile"
    mode = "r:gz"
    exts = ".tar.gz"
    magic = "gzip compressed data"

    def handles(self):
        if self.f.filename and self.f.filename.lower().endswith(self.exts):
            return True

        if not self.f.filesize:
            return False

        try:
            File(contents=gzip.GzipFile(fileobj=self.f.stream).read())
        except IOError:
            return False

        return self.magic in self.f.magic

class Tarbz2File(TarFile, Unpacker):
    name = "tarbz2file"
    mode = "r:bz2"
    exts = ".tar.bz2"

    def handles(self):
        if self.f.filename and self.f.filename.lower().endswith(self.exts):
            return True

        if not self.f.filesize:
            return False

        fd, filepath = tempfile.mkstemp()
        os.write(fd, self.f.stream.read(0x1000))
        os.close(fd)

        d = bz2.BZ2File(filepath, "r")

        try:
            ret = False
            if d.read(0x1000):
                ret = True
        except (IOError, EOFError):
            pass

        d.close()
        os.unlink(filepath)
        return ret

    def unpack(self, depth=0, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if not self.f.filepath:
            filepath = self.f.temp_path(".bz2")
            temporary = True
        else:
            filepath = self.f.filepath
            temporary = False

        f = open(os.path.join(dirpath, "output"), "wb")
        d = bz2.BZ2File(filepath, "r")

        while f.tell() < MAX_TOTAL_SIZE:
            try:
                buf = d.read(0x10000)
            except (IOError, EOFError):
                break
            if not buf:
                break
            f.write(buf)

        if temporary:
            os.unlink(filepath)

        filesize = f.tell()
        d.close()
        f.close()

        if filesize >= MAX_TOTAL_SIZE:
            self.f.set_error(
                Errors.TOTAL_TOO_LARGE,
                f"Unpacked archive size exceeds: {MAX_TOTAL_SIZE}"
            )
            return []

        return self.process_directory(dirpath, duplicates, depth)
