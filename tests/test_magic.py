# Copyright (C) 2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock import magic

def test_magic():
    assert magic.from_file("tests/files/maldoc.xls").startswith((
        "Composite Document File V2", "CDF V2 Document"
    ))
    assert magic.from_file("tests/files/test.hta_").startswith(
        "HTML document"
    )
    assert magic.from_file("tests/files/cab2.cab").startswith(
        "Microsoft Cabinet"
    )

def test_magic_exception():
    assert magic.from_file(
        "tests/files/invld.elf_"
    ).startswith("ELF")
    assert magic.from_buffer(
        open("tests/files/invld.elf_", "rb").read()
    ).startswith("ELF")
