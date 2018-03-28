# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path
import struct
import zlib

from sflock.abstracts import Unpacker, File
from sflock.exception import UnpackException

class MsoFile(Unpacker):
    name = "msofile"
    exts = b".mso"

    def supported(self):
        return True

    def get_stream(self, ole, *filename):
        if ole.exists(os.path.join(*filename)):
            return ole.openstream(os.path.join(*filename)).read()

    def locate_ole(self, contents):
        for idx in range(1024):
            try:
                obj = zlib.decompress(contents[idx:])
                break
            except:
                pass
        else:
            raise UnpackException("GZIP stream not found")

        f = File(contents=obj)
        f.raise_no_ole("No OLE file found in MSO")
        return f.ole

    def walk_stream(self, ole, name):
        try:
            ole = self.locate_ole(self.get_stream(ole, name))
        except UnpackException:
            return

        self.walk_ole(ole)

    def parse_ole10_native(self, ole, name):
        def parse_string(off):
            ret = stream[off:stream.find(b"\x00", off)]
            return off + len(ret) + 1, ret

        stream = self.get_stream(ole, "\x01Ole10Native")
        off, filename = parse_string(6)
        off, filepath = parse_string(off)
        off, tempname = parse_string(off + 8)
        embed = struct.unpack("I", stream[off:off+4])[0]
        self.entries.append(File(
            relapath=filename,
            contents=stream[off+4:off+4+embed],
            selected=False
        ))

    def walk_ole(self, ole):
        for dirname in ole.listdir():
            if dirname == ["\x01Ole10Native"]:
                self.parse_ole10_native(ole, dirname[0])
                continue

            self.walk_stream(ole, dirname[0])

    def unpack(self, password=None, duplicates=None):
        self.entries = []

        try:
            self.walk_ole(self.locate_ole(self.f.contents))
        except UnpackException as e:
            self.f.mode = "failed"
            self.f.error = e

        return self.process(self.entries, duplicates)
