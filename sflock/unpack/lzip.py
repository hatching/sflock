import os
import tempfile

from sflock.abstracts import Unpacker


class LzipFile(Unpacker):
    name = "lzip"
    exe = "/usr/bin/lzip"
    exts = b".lz"
    magic = "lzip compressed data, version: 1"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        ret = self.zipjail(
            filepath, dirpath, "-e", filepath
        )
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, password)
