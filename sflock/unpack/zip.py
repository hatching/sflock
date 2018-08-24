# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import six
import zipfile
import zlib

from sflock.abstracts import File, Unpacker
from sflock.exception import UnpackException

class ZipFile(Unpacker):
    name = "zipfile"
    exts = b".zip"
    magic = "Zip archive data"

    def supported(self):
        return True

    def handles(self):
        if super(ZipFile, self).handles():
            return True
        if self.f.stream.read(2) == b"PK":
            return True
        return False

    def decrypt(self, password, archive, entry):
        try:
            archive.setpassword(password)

            if six.PY3 and isinstance(entry.filename, str):
                entry.filename = entry.filename.encode()

            return File(
                relapath=entry.filename,
                contents=archive.read(entry),
                password=password
            )
        except (RuntimeError, zipfile.BadZipfile, OverflowError,
                zlib.error) as e:
            msg = getattr(e, "message", None) or e.args[0]
            if "Bad password" in msg:
                return
            if "Bad CRC-32" in msg:
                return
            if "password required" in msg:
                return
            if "Truncated file header" in msg:
                return
            if "invalid distance too far back" in msg:
                return
            if "cannot fit 'long' into" in msg:
                return
            if "Bad magic number for" in msg:
                return

            raise UnpackException("Unknown zipfile error: %s" % e)

    def unpack(self, password=None, duplicates=None):
        try:
            archive = zipfile.ZipFile(self.f.stream)
        except (zipfile.BadZipfile, IOError) as e:
            self.f.mode = "failed"
            self.f.error = e
            return []

        entries, directories = [], []
        for entry in archive.infolist():
            if entry.filename.endswith("/"):
                continue

            # TODO We should likely move this to self.process(), assuming
            # this is also an issue with other archive formats.
            if not entry.filename.strip():
                continue

            f = self.bruteforce(password, archive, entry)
            entries.append(f or File(
                filename=entry.filename,
                mode="failed",
                description="Error decrypting file"
            ))

            if entries[-1].relaname:
                directories.append(os.path.dirname(entries[-1].relaname))

        # This fixes an issue when a directory name is identified as "foo"
        # instead of "foo/" as required by zipfile (and likely the majority
        # of other .zip implementations). The issue being "foo" being created
        # as an empty file rather than a directory.
        # TODO We should likely move this to self.process(), assuming this
        # is also an issue with other archive formats.
        for idx, entry in enumerate(entries[:]):
            if entry.relaname in directories:
                entries.pop(idx)

        return self.process(entries, duplicates)
