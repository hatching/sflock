# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.decode.office import Office

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def test_decode_docx():
    assert Office(f("encrypted1.docx"), "Password1234_").decrypt().magic in (
        "Microsoft Word 2007+", "Zip archive data, at least v2.0 to extract"
    )

def test_decode_regular():
    assert Office(f("maldoc/0882c8"), "").decrypt() is None
