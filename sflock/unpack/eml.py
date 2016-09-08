# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import email
import email.header

from sflock.abstracts import Unpacker, File
from sflock.pick import picker

class EmlFile(Unpacker):
    name = "emlfile"
    exts = ".eml"

    whitelisted_content_type = [
        "text/plain", "text/html",
    ]

    def supported(self):
        return True

    def handles(self):
        return picker(self.f.filepath) == self.name

    def unpack(self, password=None, duplicates=None):
        entries = []

        e = email.message_from_string(self.f.contents)
        for part in e.walk():
            if part.is_multipart():
                continue

            if not part.get_filename() and \
                    part.get_content_type() in self.whitelisted_content_type:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            filename = part.get_filename()
            if filename:
                filename = unicode(email.header.make_header(
                    email.header.decode_header(filename)
                ))

            entries.append(File(filename or "att1", payload))

        return self.process(entries, duplicates)
