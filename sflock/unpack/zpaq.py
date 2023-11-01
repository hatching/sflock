# Copyright (C) 2016 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import tempfile
import subprocess
from sflock.abstracts import Unpacker


class ZpaqFile(Unpacker):
    name = "zpaq"
    exe = "/usr/bin/zpaq"
    exts = b".zpaq"
    magic = "ZPAQ file"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()
        original_path = self.f.filepath
        if self.f.filepath:
            if not self.f.filepath.endswith(b".zpaq"):
                os.rename(self.f.filepath, self.f.filepath + b".zpaq")
                self.f.filepath = self.f.filepath + b".zpaq"
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(b".zpaq")
            temporary = True

        # ToDo fix tracy/zipjail Blocked mmap(2) syscall with X flag set!
        # ret = self.zipjail(filepath, dirpath, "x", filepath, "-to", dirpath + os.sep)

        p = subprocess.Popen(
            (self.exe, "x", filepath, "-to", dirpath),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return_code = p.wait()
        _, _ = p.communicate()
        ret = not return_code

        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        if original_path != self.f.filepath:
            os.rename(self.f.filepath, original_path)
            self.f.filepath = original_path

        return self.process_directory(dirpath, duplicates)

"""
from sflock import unpack
q = unpack(b"1c33eef0d22dc54bb2a41af485070612cd4579529e31b63be2141c4be9183eb6.zpaq")
q.to_dict()
"""
