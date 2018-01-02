# Copyright (C) 2015-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

# Authors: Ryan Borre, Devin Smith, and Kyle Fenzel
# Basic VBN carving program built to take in a VBN file
# and parse it out to produce the original file
# Based on a script originally written by Ryan Borre


from sflock.abstracts import Unpacker, File
from io import BytesIO
from struct import unpack_from

class VBNFile(Unpacker):
    name = "vbnfile"
    exts = ".vbn"

    def supported(self):
        if self.f.contents[0xb8c:0xb96] == "FileSystem":
            return True
        return False

    def unpack(self, password=None, duplicates=None):
        vbn_file = self.f.contents
        file_name = vbn_file[0x4:0x183].split("\x00")[0].split("\\")[-1]
        file_data = vbn_file[0x1290:]
        file_size = unpack_from("<I", vbn_file, 0xd54)[0]
        chunk_offset = 65536
        chunk_size = 5
        chunks = 0
        xor_key = unpack_from("<B", vbn_file[0x1292])[0]
        config_xor_key = 0x5a
        decoded_bytes = bytearray()
        config_bytes = bytearray()
        chunk_bytes = bytearray()

        # determine the Xor key
        if xor_key == 0x5a:
            xor_key = 0xa5
        elif xor_key == 0xa5:
            xor_key = 0x5a
        else:
            xor_key = 0x5a

        # decode the config and file
        for i in range(len(file_data)):
            config_bytes.append(ord(file_data[i]) ^ config_xor_key)
            decoded_bytes.append(ord(file_data[i]) ^ xor_key)

        # ata was encrypted with 0x5a
        if xor_key == 0x5a:
            chunk_bytes = decoded_bytes[-file_size:]

        # data was encrypted with 0xa5
        if xor_key == 0xa5:
            offset = config_bytes.find("\x03\x03\x00\x00\x00\x0A\x01\x08") + 0x76
            offset_size = unpack_from("<I", config_bytes, offset)[0]
            file_offset_ratio = len(file_data) / offset_size

            #TODO may need to implement explicitly for VBN inside of a VBN
            # handle VBN within a VBN
            # if file_name.endswith(".vbn"):
            #     config_size = offset + 0x4
            #     decoded_bytes = decoded_bytes[config_size:]
            #     offset = unpack_from("<I", decoded_bytes, 0x8)[0]
            #     offset += 0x1c
            #     file_size = unpack_from("<I", decoded_bytes, offset)[0]
            #     offset += 0xc
            #     chunk_bytes = decoded_bytes[offset:offset + file_size]

            # file size not in config
            if offset_size == chunk_offset or file_offset_ratio == 1:
                config_size = offset + 0x4
                decoded_bytes = decoded_bytes[config_size:]
                offset = unpack_from("<I", decoded_bytes, 0x8)[0]
                offset += 0x1c
                file_size = unpack_from("<I", decoded_bytes, offset)[0]
                offset += 0xc
                chunks = (file_size / chunk_offset) * chunk_size
                file_size += chunks
                chunk_bytes = decoded_bytes[offset:offset + file_size]
            # file size in config
            elif file_offset_ratio > 1:
                offset += offset_size + 0xa
                file_size = unpack_from("<I", config_bytes, offset)[0]
                offset += 0xd
                chunks = (file_size / chunk_offset) * chunk_size
                file_size += chunks
                chunk_bytes = decoded_bytes[offset:offset + file_size]
            #
            else:
                return self.process([], duplicates)

        # file is not chunked
        if chunks == 0:
           chunk_size = 0

        io_bytes = BytesIO(chunk_bytes)
        file_bytes = bytearray()

        # remove chunked bytes
        while io_bytes.tell() < len(io_bytes.getvalue()):
            file_bytes += io_bytes.read(chunk_offset)
            io_bytes.read(chunk_size)

        entries = []

        # store data as sflock File type
        entries.append(File(
            relapath=file_name,
            contents=BytesIO(file_bytes).read()
        ))

        return self.process(entries, duplicates)