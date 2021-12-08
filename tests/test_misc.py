# Copyright (C) 2016-2018 Jurriaan Bremer.
# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.misc import make_list


def test_make_list():
    assert make_list(None) == [None]
    assert make_list([]) == []
    assert make_list(()) == []
    assert make_list(1) == [1]
    assert make_list("a") == ["a"]
    assert make_list((1, 2)) == [1, 2]
    assert make_list([3, 4]) == [3, 4]
