# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.decode.office import Office
from sflock.main import unpack

def f(filename):
    return File.from_path("tests/files/%s" % filename)

def f2(filename):
    return "tests/files/%s" % filename

def test_decode_docx():
    assert Office(f("encrypted1.docx"), "Password1234_").decode().magic in (
        "Microsoft Word 2007+", "Zip archive data, at least v2.0 to extract"
    )
    # Invalid password provided.
    assert Office(f("encrypted1.docx"), "Password12345").decode() is False

def test_decode_regular():
    assert Office(f("maldoc/0882c8"), "").decode() is None

def test_passwords():
    assert len(unpack(f2("zip_encrypted.zip")).children) == 1

    z = unpack(f2("zip_encrypted2.zip"))
    assert not z.children[0].magic

    z = unpack(f2("zip_encrypted2.zip"), password=b"sflock")
    assert z.children[0].magic == "ASCII text"

    z = unpack(f2("zip_encrypted2.zip"), password=[b"sflock"])
    assert z.children[0].magic == "ASCII text"
