# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.unpack.tar import Tarfile
from sflock.unpack.zip import Zipfile

class Signatures:
    signatures = {
        "\x50\x4B": {
            "unpacker": Zipfile,
            "mode": "",
            "family": "zip"
        },
        "\x75\x73\x74\x61\x72\x20\x20\x00": {
            "unpacker": Tarfile,
            "mode": "r:*",
            "family": "tar"
        },
        "\x42\x5A\x68": {
            "unpacker": Tarfile,
            "mode": "r:bz2",
            "family": "tar"
        },
        "\x1F\x8B": {
            "unpacker": Tarfile,
            "mode": "r:gz",
            "family": "tar"
        }
    }