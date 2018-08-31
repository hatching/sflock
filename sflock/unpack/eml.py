# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import email
import email.header
import re
import six

from sflock.abstracts import Unpacker, File

class EmlFile(Unpacker):
    name = "emlfile"
    exts = b".eml"

    whitelisted_content_type = [
        "text/plain", "text/html",
    ]

    def supported(self):
        return True

    def handles(self):
        if super(EmlFile, self).handles():
            return True

        stream = self.f.stream
        keys = []
        for _ in range(10):
            line = stream.readline()
            if b":" in line:
                keys.append(line.split(b":")[0])
        if b"From" in keys and b"To" in keys:
            return True
        return False

    def real_unpack(self, password, duplicates):
        entries = []

        if six.PY3:
            e = email.message_from_string(self.f.contents.decode("latin-1"))
        else:
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

            if six.PY2 and filename:
                filename = unicode(email.header.make_header(
                    email.header.decode_header(filename)
                )).encode('utf-8')
            if six.PY3 and filename:
                filename = email.header.make_header(
                    email.header.decode_header(filename)
                )
                filename = str(filename).encode()

            entries.append(File(
                relapath=filename or b"att1", contents=payload
            ))

        return entries

    def unpack(self, password=None, duplicates=None):
        re_compile_orig = re.compile

        def re_compile_our(pattern):
            return re_compile_orig(pattern.replace("?P<end>--", "?P<end>--+"))

        if six.PY2:
            re.compile = re_compile_our

        try:
            entries = self.real_unpack(password, duplicates)
        finally:
            re.compile = re_compile_orig

        return self.process(entries, duplicates)
