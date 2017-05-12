# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.exception import DecoderException
from sflock.decode.office import Office

def f(filename):
    return File.from_path("tests/files/%s" % filename)

@pytest.mark.skipif("sys.platform == 'linux2'")
def test_no_pycrypto():
    with pytest.raises(DecoderException) as e:
        assert Office(None, None)
    e.match("manually installing PyCrypto")

@pytest.mark.skipif("sys.platform != 'linux2'")
def test_decode_docx():
    assert Office(f("encrypted1.docx"), "Password1234_").decrypt().magic in (
        "Microsoft Word 2007+", "Zip archive data, at least v2.0 to extract"
    )

@pytest.mark.skipif("sys.platform != 'linux2'")
def test_decode_regular():
    assert Office(f("maldoc/0882c8"), "").decrypt() is None
