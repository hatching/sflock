# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import bz2
import gzip
import os
import shutil
import six
import tarfile
import tempfile

from sflock.abstracts import Unpacker, File
from sflock.config import MAX_TOTAL_SIZE


class TarFile(Unpacker):
    name = "tarfile"
    mode = "r:"
    exts = b".tar"
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

        entries, total_size = [], 0
        for entry in archive:
            # Ignore anything that's not a file for now.
            if not entry.isfile() or entry.size < 0:
                continue

            # TODO Improve this. Also take precedence for native decompression
            # utilities over the Python implementation in the future.
            total_size += entry.size
            if total_size >= MAX_TOTAL_SIZE:
                self.f.error = "files_too_large"
                return []

            relapath = entry.path
            if six.PY3:
                relapath = relapath.encode()

            entries.append(File(
                relapath=relapath,
                contents=archive.extractfile(entry).read()
            ))

        return self.process(entries, duplicates)

class TargzFile(TarFile, Unpacker):
    name = "targzfile"
    mode = "r:gz"
    exts = b".tar.gz"

    def supported(self):
        return True

    def handles(self):
        ret = False
        if self.f.filename and self.f.filename.lower().endswith(b".tar.gz"):
            return True

        if not self.f.filesize:
            return ret

        fd, filepath = tempfile.mkstemp()
        os.write(fd, self.f.stream.read(0x1000))
        os.close(fd)

        d = gzip.open(filepath)

        try:
            ret = False
            if d.read(0x1000):
                ret = True
        except IOError:
            pass

        d.close()
        os.unlink(filepath)
        return ret


    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if not self.f.filepath:
            filepath = self.f.temp_path(".gz")
            temporary = True
        else:
            filepath = self.f.filepath
            temporary = False

        outfile = open(os.path.join(dirpath, "output"), 'wb')
        with gzip.open(filepath) as infile:
            try:
                while True:
                    chunk = infile.read(0x10000)
                    if not chunk:
                        break
                    outfile.write(chunk)
            except gzip.zlib.error:
                pass

        outfile.close()

        if temporary:
            os.unlink(filepath)
        return self.process_directory(dirpath, duplicates)


class Tarbz2File(TarFile, Unpacker):
    name = "tarbz2file"
    mode = "r:bz2"
    exts = b".tar.bz2"

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
        except IOError:
            pass

        d.close()
        os.unlink(filepath)
        return ret

    def unpack(self, password=None, duplicates=None):
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
            except IOError:
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
            self.f.error = "files_too_large"
            return []

        return self.process_directory(dirpath, duplicates)

