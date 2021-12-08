# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.decode.office import Office
from sflock.errors import Errors
from sflock.main import unpack


def f(filename):
    return File.from_path("tests/files/%s" % filename)


def f2(filename):
    return "tests/files/%s" % filename


def test_decode_docx():
    assert Office(f(b"encrypted1.docx"), "Password1234_").decode().magic in (
        "Microsoft Word 2007+",
        "Zip archive data, at least v2.0 to extract",
    )
    # Invalid password provided.
    assert Office(f("encrypted1.docx"), "Password12345").decode() is False


def test_decode_regular():
    assert Office(f("maldoc/0882c8"), "").decode() is None


def test_passwords():
    f = unpack(f2("zip_encrypted.zip"))
    assert len(f.children) == 1
    assert f.children[0].filesize == 21

    # Give no password. Should result in error
    z = unpack(f2("zip_encrypted2.zip"))
    assert z.mode == Errors.DECRYPTION_FAILED

    z = unpack(f2(b"zip_encrypted2.zip"), password="sflock")
    assert z.children[0].magic == "ASCII text"

def test_decode_xlsx():
    z = unpack(f2("xlsx_encoded.xlsx")).children
    assert len(z) == 2
    filenames = [x.filename for x in z]
    assert "EncryptionInfo" in filenames
    assert "EncryptedPackage" in filenames
