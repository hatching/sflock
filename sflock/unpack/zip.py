# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import zipfile
from StringIO import StringIO

from sflock.abstracts import File, Unpacker
from sflock.config import iter_passwords
from sflock.exception import UnpackException

class Zipfile(Unpacker):
    name = "zipfile"
    author = ["Jurriaan Bremer", "Sander Ferdinand"]

    def init(self):
        self.known_passwords = set()

    def handles(self):
        if self.f.filepath:
            return zipfile.is_zipfile(self.f.filepath)
        else:
            return self._is_zipfile(self.f.contents)

    def _bruteforce(self, archive, entry, passwords):
        for password in passwords:
            try:
                archive.setpassword(password)
                ret = File(entry.filename, archive.read(entry),
                           password=password)
                self.known_passwords.add(password)
                return ret
            except (RuntimeError, zipfile.BadZipfile) as e:
                msg = e.message or e.args[0]
                if "Bad password" not in msg and "Bad CRC-32" not in msg:
                    raise UnpackException("Unknown zipfile error: %s" % e)

    def _decrypt(self, archive, entry, password):
        try:
            archive.setpassword(password)
            return File(entry.filename, archive.read(entry),
                        password=password)
        except RuntimeError as e:
            if "password required" not in e.args[0] and \
                    "Bad password" not in e.args[0]:
                raise UnpackException("Unknown zipfile error: %s" % e)

        # Bruteforce the password. First try all passwords that are known to
        # work and if that fails try our entire dictionary.
        return (
            self._bruteforce(archive, entry, self.known_passwords) or
            self._bruteforce(archive, entry, iter_passwords()) or
            File(entry.filename, None, mode="failed",
                 description="Error decrypting file")
        )

    def unpack(self, mode=None, password=None):
        if self.f.filepath:
            archive = zipfile.ZipFile(self.f.filepath)
        else:
            archive = zipfile.ZipFile(StringIO(self.f.contents))

        for entry in archive.infolist():
            yield self.parse_item(self._decrypt(archive, entry, password))

    def _is_zipfile(self, contents=None):
        if contents.startswith("\x50\x4b"):
            return True
