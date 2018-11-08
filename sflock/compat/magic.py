# Copyright (C) 2016-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from __future__ import absolute_import

import logging
import os
import sys

import sflock

from sflock.misc import data_file

log = logging.getLogger(__name__)

# Provide libmagic support in terms of binaries under Windows.
if sys.platform == "win32":
    if sys.maxsize != 0x7fffffff:
        os.environ["PATH"] = "%s;%s" % (
            data_file("win64"), os.environ["PATH"]
        )
        magic_file = data_file("win64", "magic.mgc")
    else:
        os.environ["PATH"] = "%s;%s" % (
            data_file("win32"), os.environ["PATH"]
        )
        magic_file = data_file("win32", "magic.mgc")

# Therefore only import libmagic at this point.
import magic

if sys.platform == "win32":
    magic._instances[False] = magic.Magic(mime=False, magic_file=magic_file)
    magic._instances[True] = magic.Magic(mime=True, magic_file=magic_file)

def from_file(f, mime=False):
    try:
        return magic.from_file(f, mime)
    except magic.MagicException as e:
        return e.message

def from_buffer(buf, mime=False):
    try:
        return magic.from_buffer(buf, mime)
    except magic.MagicException as e:
        return e.message
