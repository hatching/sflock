# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import ntpath
import six.moves

from sflock.abstracts import Unpacker, File

class BupFile(Unpacker):
    name = "bupfile"
    exts = b".bup"

    def supported(self):
        return True

    def handles(self):
        if super(BupFile, self).handles():
            return True

        if self.f.ole and ["Details"] in self.f.ole.listdir():
            return True
        return False

    def decrypt(self, content):
        return b"".join(b"%c" % (ch ^ 0x6a) for ch in content)

    def unpack(self, password=None, duplicates=None):
        entries = []

        if not self.f.ole:
            self.f.mode = "failed"
            self.f.error = "No OLE structure found"
            return []

        if ["Details"] not in self.f.ole.listdir():
            return []

        details = self.decrypt(
            bytearray(self.f.ole.openstream("Details").read())
        )

        config = six.moves.configparser.ConfigParser()
        if six.PY3:
            config.read_string(details.decode())
        else:
            config.readfp(io.BytesIO(details))

        ole = self.f.ole

        for filename in ole.listdir():
            if filename[0] == "Details" or not ole.get_size(filename[0]):
                continue

            relapath = ntpath.basename(
                config.get(filename[0], "OriginalName")
            )
            if six.PY3:
                relapath = relapath.encode()

            entries.append(File(
                relapath=relapath,
                contents=self.decrypt(
                    bytearray(ole.openstream(filename[0]).read())
                )
            ))

        return self.process(entries, duplicates)
