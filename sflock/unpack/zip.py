# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import stat
import zipfile
import zlib

from sflock.abstracts import File, Unpacker
from sflock.config import MAX_TOTAL_SIZE
from sflock.exception import (
    UnpackException, DecryptionFailedError, NotSupportedError
)
from sflock.errors import Errors

class InvalidZipEntryError(UnpackException):
    pass

class ZipFile(Unpacker):
    name = "zipfile"
    exts = ".zip"
    magic = "Zip archive data"

    def supported(self):
        return True

    def handles(self):
        if self.f.stream.read(2) == b"PK":
            try:
                z = zipfile.ZipFile(self.f.stream)
            except (zipfile.BadZipFile, IOError):
                return False

            infos = z.infolist()
            if not infos:
                return False

            # Assume all entries are the same compression type. We do not
            # support multiple compress or encryption types per archive.
            if infos[0].compress_type in (zipfile.ZIP_DEFLATED,
                                          zipfile.ZIP_STORED,
                                          zipfile.ZIP_BZIP2, zipfile.ZIP_LZMA):
                return True

        return False

    def decrypt(self, password, archive, entry):
        try:
            if password:
                archive.setpassword(password.encode())

            relapath = entry.filename.lstrip("/")
            if not relapath:
                raise InvalidZipEntryError(
                    "Filename empty after stripping absolute path"
                )

            return File(
                relapath=relapath,
                contents=archive.read(entry),
                password=password
            )
        except (RuntimeError, zipfile.BadZipFile, OverflowError,
                zlib.error, UnicodeDecodeError) as e:
            msg = getattr(e, "message", None) or e.args[0]

            if any(x in msg for x in ("Bad password", "password required")):
                raise DecryptionFailedError(
                    "No correct password for encrypted archive"
                )

            if any(x in msg for x in (
                    "compression method is not supported",
                    "compression type 99"
            )):
                raise NotSupportedError(
                    "7z is required to unpack this ZIP archive"
                )

            skippable = ("Bad CRC-32", "Truncated file header",
                         "invalid distance too far back",
                         "cannot fit 'long' into", "Bad magic number for")

            if any(x in msg for x in skippable):
                raise InvalidZipEntryError(msg)

            raise UnpackException(f"Unknown zipfile error: {e}")

    def unpack(self, depth=0, password=None, duplicates=None):
        self.f.archive = True
        try:
            archive = zipfile.ZipFile(self.f.stream)
        except (zipfile.BadZipFile, IOError) as e:
            self.f.set_error(Errors.INVALID_ARCHIVE, str(e))
            return []

        entries, directories, total_size = [], [], 0

        illegal = ("..", ":", "\x00")
        for entry in archive.infolist():
            if entry.filename.endswith("/") or entry.file_size < 0:
                continue

            # TODO We should likely move this to self.process(), assuming
            # this is also an issue with other archive formats.
            if not entry.filename.strip():
                continue

            if any(c in entry.filename for c in illegal):
                raise UnpackException(
                    f"Illegal character(s) in file path",
                    Errors.CANCELLED_DIR_TRAVERSAL
                )

            if stat.S_ISLNK(entry.external_attr >> 16):
                raise UnpackException(
                    "Cancelled: symlink creation attempt detected",
                    Errors.CANCELLED_SYMLINK
                )

            # TODO Improve this. Also take precedence for native decompression
            # utilities over the Python implementation in the future.
            total_size += entry.file_size
            if total_size >= MAX_TOTAL_SIZE:
                self.f.set_error(
                    Errors.TOTAL_TOO_LARGE,
                    f"Unpacked archive size exceeds maximum of: "
                    f"{MAX_TOTAL_SIZE}"
                )
                return []

            try:
                f = self.bruteforce(password, archive, entry)
                # We stop unpacking if decryption of one entry failed and
                # we have tried all passwords.
            except InvalidZipEntryError as e:
                # We do not stop unpacking if an entry in the archive is
                # invalid. Mark the invalid entry and continue.
                f = File(filename=entry.filename, mode="failed")
                f.error = str(e)

            entries.append(f)
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

        return self.process(entries, duplicates, depth)
