# Copyright (C) 2016-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import olefile

from sflock.abstracts import Unpacker, File

class MsgFile(Unpacker):
    name = "msgfile"
    exts = ".msg"

    def supported(self):
        return True

    def get_stream(self, *filename):
        if self.ole.exists("/".join(filename)):
            return self.ole.openstream("/".join(filename)).read()

    def get_string(self, *filename):
        ascii_filename = "%s001E" % "/".join(filename)
        unicode_filename = "%s001F" % "/".join(filename)

        # If available, the unicode stream takes precedence.
        stream = self.get_stream(unicode_filename)
        if stream:
            return stream.decode("utf16")

        return self.get_stream(ascii_filename)

    def get_attachment(self, dirname):
        filename = (
            self.get_string(dirname, "__substg1.0_3707") or
            self.get_string(dirname, "__substg1.0_3704") or
            "att1"
        )
        contents = self.get_stream(dirname, "__substg1.0_37010102")
        return filename, contents

    def unpack(self, password=None, duplicates=None):
        seen, entries = [], []

        try:
            self.ole = olefile.OleFileIO(self.f.stream)
        except IOError as e:
            self.f.mode = "failed"
            self.f.error = e
            return []

        for dirname in self.ole.listdir():
            if dirname[0].startswith("__attach") and dirname[0] not in seen:
                filename, contents = self.get_attachment(dirname[0])
                entries.append(File(
                    relapath=filename, contents=contents
                ))
                seen.append(dirname[0])

        return self.process(entries, duplicates)
