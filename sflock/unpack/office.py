# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import Unpacker
from sflock.decode import plugins

class OfficeFile(Unpacker):
    name = "office"
    package = "doc", "xls", "ppt"
    magic = ["Composite Document File", "CDFV2 Encrypted"]

    def supported(self):
        return True

    def decrypt(self, password):
        if password is None:
            return

        return plugins["office"](self.f, password).decode()

    def unpack(self, depth=0, password=None, duplicates=None):
        # Avoiding recursive imports. TODO Can this be generalized?
        from sflock import ident

        entries = []

        f = self.bruteforce(password)
        if f:
            entries.append(f)

        ret = self.process(entries, duplicates, depth)
        f and ident(f)
        return ret
