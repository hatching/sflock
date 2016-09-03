# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

class Signatures:
    signatures = {
        "\x50\x4b": {
            "unpacker": "zipfile",
            "mode": "",
            "family": "zip"
        },
        "\x75\x73\x74\x61\x72\x20\x20\x00": {
            "unpacker": "tarfile",
            "mode": "r:*",
            "family": "tar"
        },
        "\x42\x5a\x68": {
            "unpacker": "tarbz2file",
            "mode": "r:bz2",
            "family": "tar"
        },
        "\x1f\x8b": {
            "unpacker": "targzfile",
            "mode": "r:gz",
            "family": "tar"
        }
    }
