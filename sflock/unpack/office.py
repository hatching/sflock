# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import Unpacker
from sflock.decode import plugins
from sflock.exception import DecoderException

class OfficeFile(Unpacker):
    name = "office"
    package = "doc", "xls", "ppt"

    def supported(self):
        return True

    def decrypt(self, password):
        if password is None:
            return

        try:
            d = plugins["office"](self.f, password)
        except DecoderException:
            # TODO Should this be moved to the supported() method?
            self.f.mode = "failed"
            self.f.error = (
                "To decrypt a Microsoft Office document PyCrypto is required!"
            )
            return

        return d.decode()

    def unpack(self, password=None, duplicates=None):
        entries = []

        f = self.bruteforce(password)
        if f:
            entries.append(f)
            self.f.preview = True
            self.f.selected = False

        return self.process(entries, duplicates)
