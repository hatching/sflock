# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import json
import os

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import plugins

def f(filename):
    return File.from_path(os.path.join(b"tests", b"files", filename))

def test_attributes():
    for filename in os.listdir(b"tests/files"):
        if os.path.isdir(b"tests/files/%s" % filename):
            continue

        if b"encrypted" in filename:
            continue

        f = unpack(b"tests/files/%s" % filename)
        assert json.loads(json.dumps(list(f.to_dict()))) == list(f.to_dict())

def test_unpack_not_none():
    for filename in os.listdir(b"tests/files"):
        if os.path.isdir(b"tests/files/%s" % filename):
            continue

        for unpacker in plugins.values():
            if not unpacker(None).supported():
                continue
            assert unpacker(f(filename)).unpack() is not None
