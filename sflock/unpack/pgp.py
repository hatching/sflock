# Copyright (C) 2016 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker


class PGP(Unpacker):
    name = "pgpfile"
    exe = "/usr/bin/gpg"
    exts = b".pgp", b".gpg"
    magic = "PGP "

    def unpack(self, password: str = None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True
        # ToDo
        # locked system call occurred during sandboxing!\nip=0x7f9d2bc0fa97 sp=0x7ffdcb8d5eb8 abi=0 nr=102 syscall=getuid
        # ret = self.zipjail(filepath, dirpath, "-o", os.path.join(dirpath, "extracted"), "--passphrase=%s" % (password or ""), filepath)
        p = subprocess.Popen(
            (self.exe, "--decrypt", "--batch", "-o", os.path.join(dirpath, "extracted"), "--passphrase=%s" % (password or ""), filepath),
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

        return self.process_directory(dirpath, duplicates, password)
