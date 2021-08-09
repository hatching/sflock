# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path

from sflock.abstracts import File
from sflock.main import unpack
from sflock.ident import identify

def f(filename):
    return os.path.join(b"tests", b"files", filename)


def test_shellcode64_plain():
    t = unpack(f(b"shellcode.zip"))
    assert identify(t.children[0]) == "Shellcode_x64"
