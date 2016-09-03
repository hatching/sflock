# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import shutil
import subprocess
import tempfile

from sflock.abstracts import Unpacker, File
from sflock.exception import UnpackException

class Rarfile(Unpacker):
    name = "rarfile"
    exe = "/usr/bin/rar"
    exts = ".rar"

    def handles(self):
        return "RAR archive" in self.f.magic

    def unpack(self, duplicates=None):
        dirpath = tempfile.mkdtemp()

        try:
            subprocess.check_call([
                self.zipjail, self.f.filepath, dirpath,
                self.exe, "x", "-mt1", self.f.filepath, dirpath,
            ])
        except subprocess.CalledProcessError as e:
            raise UnpackException(e)

        entries = []
        duplicates = duplicates or []
        for dirpath2, dirnames, filepaths in os.walk(dirpath):
            for filepath in filepaths:
                filepath = os.path.join(dirpath2, filepath)
                f = File.from_path(
                    filepath, filename=filepath[len(dirpath)+1:],
                )

                if f.sha256 not in duplicates:
                    duplicates.append(f.sha256)
                else:
                    f.duplicate = True

                entries.append(f)

        shutil.rmtree(dirpath)
        return self.process(entries, duplicates)
