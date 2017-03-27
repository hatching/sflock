# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.pick import package

def test_malformed_rtf():
    hashes = [
        "0882c8a38ca485fe9763b0c0c7c5a22c330cebe86101a9e1ffa5a70c4f58faac",
        "11836837753c754997adf8ccf4fa8ba824e57725f56fbcd3b0d903e1fa30ac5b",
    ]
    assert package(File("tests/files/maldoc/%s" % hashes[0])) == "doc"
    assert package(File("tests/files/maldoc/%s" % hashes[1])) == "doc"
