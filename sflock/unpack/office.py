# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import Unpacker
from sflock.decode import plugins

class OfficeFile(Unpacker):
    name = "office"
    package = "doc", "xls", "ppt"

    def supported(self):
        return True

    def decrypt(self, password):
        if password is None:
            return

        return plugins["office"](self.f, password).decode()

    def unpack(self, password=None, duplicates=None):
        entries = []

        f = self.bruteforce(password)
        if f:
            entries.append(f)
            self.f.preview = True
            self.f.selected = False

        return self.process(entries, duplicates)
