# Copyright (C) 2016-2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import json
import os

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import plugins

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_attributes():
    for filename in os.listdir("tests/files"):
        if os.path.isdir("tests/files/%s" % filename):
            continue

        if "encrypted" in filename:
            continue

        f = unpack("tests/files/%s" % filename)
        assert json.loads(json.dumps(f.to_dict())) == f.to_dict()

def test_unpack_not_none():
    for filename in os.listdir("tests/files"):
        if os.path.isdir("tests/files/%s" % filename):
            continue

        for unpacker in plugins.values():
            if not unpacker(None).supported():
                continue
            assert unpacker(f(filename)).unpack() is not None
