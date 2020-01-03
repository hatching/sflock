# Copyright (C) 2016 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker

class VHDFile(Unpacker):
    name = "vhdfile"
    exts = b".vhd"
    magic = " Microsoft Disk Image"

    def unpack(self, password=None, duplicates=None):
        try:
            from guestfs import GuestFS
        except ImportError:
            print("missed guestfs library. pip3 install http://download.libguestfs.org/python/guestfs-1.40.2.tar.gz or newer")
            return []

        if self.f.filepath:
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(".vhd")
            temporary = True

        dirpath = tempfile.mkdtemp()
        g = GuestFS(python_return_dict=True)
        g.add_drive_opts(filepath, readonly=1)
        g.launch()
        try:
            g.mount_ro("/dev/sda1", "/")
        except RuntimeError as msg:
            log.error("Error mounting Microsoft Disk Image: {} - {}".format((filepath, msg)))
            g.close()
            return []

        files = g.ls("/")
        if files:
            g.copy_out("/", tmp_dir)
        g.umount_all()
        g.close()

        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)
