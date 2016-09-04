# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.unpack import EmlFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

class TestEmlFile(object):
    def test_eml_tar_nested2(self):
        assert "SMTP mail" in f("eml_tar_nested2.eml").magic
        t = EmlFile(f("eml_tar_nested2.eml"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 1
        assert files[0].filepath == "tar_nested2.tar"
        assert "POSIX tar" in files[0].magic

        assert len(files[0].children) == 1
        assert files[0].children[0].contents == "hello world\n"
        assert files[0].children[0].magic == "ASCII text"
        assert files[0].children[0].parentdirs == ["deepfoo", "foo"]
