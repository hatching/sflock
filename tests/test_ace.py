# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.unpack import AceFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

class TestAceFile(object):
    def test_ace_plain(self):
        assert "ACE archive" in f("ace_plain.ace").magic
        t = AceFile(f("ace_plain.ace"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 1
        assert files[0].filepath == "ace.txt"
        assert files[0].contents == "wow .ace"
        assert "ASCII text" in files[0].magic
        assert files[0].parentdirs == []

        # TODO A combination of file extension, file magic, and initial bytes
        # signature should be used instead of just the bytes (as this call
        # should not yield None).
        assert f("ace_plain.ace").get_signature() is None

    def test_nested_plain(self):
        assert "ACE archive" in f("ace_nested.ace").magic
        t = AceFile(f("ace_nested.ace"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].filepath == "b00/ace.txt"
        assert files[0].parentdirs == ["b00"]
        assert files[0].contents == "wow .ace"
        assert not files[0].password
        assert "ASCII text" in files[0].magic

        s = f("ace_nested.ace").get_signature()
        assert s is None

    def test_nested2_plain(self):
        assert "ACE archive" in f("ace_nested2.ace").magic
        t = AceFile(f("ace_nested2.ace"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 1

        assert files[0].filepath == "derp/b00/ace.txt"
        assert files[0].parentdirs == ["derp", "b00"]
        assert files[0].contents == "wow .ace"
        assert not files[0].password
        assert "ASCII text" in files[0].magic

        s = f("ace_nested2.ace").get_signature()
        assert s is None
