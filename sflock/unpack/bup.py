# Copyright (C) 2016-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import ConfigParser
import io
import ntpath

from sflock.abstracts import Unpacker, File

class BupFile(Unpacker):
    name = "bupfile"
    exts = ".bup"

    def supported(self):
        return True

    def handles(self):
        if super(BupFile, self).handles():
            return True

        if self.f.ole and ["Details"] in self.f.ole.listdir():
            return True
        return False

    def decrypt(self, content):
        return "".join(chr(ord(ch) ^ 0x6a) for ch in content)

    def unpack(self, password=None, duplicates=None):
        entries = []

        if not self.f.ole:
            self.f.mode = "failed"
            self.f.error = "No OLE structure found"
            return []

        details = self.decrypt(self.f.ole.openstream("Details").read())
        config = ConfigParser.ConfigParser()
        config.readfp(io.BytesIO(details))

        ole = self.f.ole

        for filename in ole.listdir():
            if filename[0] == "Details" or not ole.get_size(filename[0]):
                continue

            entries.append(File(
                relapath=ntpath.basename(
                    config.get(filename[0], "OriginalName")
                ),
                contents=self.decrypt(ole.openstream(filename[0]).read())
            ))

        return self.process(entries, duplicates)
