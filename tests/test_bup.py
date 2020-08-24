# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os.path

from sflock.abstracts import File
from sflock.unpack import BupFile

def f(filename):
    return File.from_path(os.path.join("tests", "files", filename))

def test_bup_plain():
    assert f("bup_test.bup").magic.startswith((
        "Composite Document File V2", "CDF V2 Document"
    ))
    t = BupFile(f("bup_test.bup"))
    assert t.handles() is True
    assert not t.f.selected
    files = list(t.unpack())

    assert len(files) == 1
    assert not files[0].filepath
    assert files[0].relapath == "efax_9057733019_pdf.zip"
    assert "Zip archive" in files[0].magic
    assert files[0].parentdirs == []
    assert files[0].extension == "zip"
    assert files[0].platforms == [
                        {"platform": "windows", "os_version": ""},
                        {"platform": "darwin", "os_version": ""},
                        {"platform": "linux", "os_version": ""},
                        {"platform": "android", "os_version": ""},
                        {"platform": "ios", "os_version": ""}
                    ]
    assert not files[0].selected

    assert len(files[0].children) == 1
    assert not files[0].children[0].filepath
    assert files[0].children[0].relapath == "efax_9057733019_pdf.scr"
    assert files[0].children[0].filesize == 377856
    assert files[0].children[0].extension == "exe"
    assert files[0].children[0].platforms == [{"platform": "windows", "os_version": ""}]
    assert files[0].children[0].selected is True

def test_garbage():
    t = BupFile(f("garbage.bin"))
    assert t.handles() is False
    assert not t.f.selected
    assert not t.f.identified
    assert not t.unpack()
    assert t.f.mode == "failed"
