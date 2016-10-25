# Copyright (C) 2016 Jurriaan Bremer.
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
        log.warning("libmagic is not supported on 64-bit Python on Windows")
        supported = False
    else:
        supported = True

        os.environ["PATH"] = "%s;%s" % (
            data_file("win32"), os.environ["PATH"]
        )
else:
    supported = True

# Therefore only import libmagic at this point.
if supported:
    import magic

def patch():
    """Patch libmagic to use our magic.mgc file, so that it the same across
    multiple operating systems, Linux distributions, etc."""
    if sys.platform != "win32" or magic._instances:
        return

    magic._instances[False] = magic.Magic(
        mime=False, magic_file=data_file("win32", "magic.mgc")
    )

    magic._instances[True] = magic.Magic(
        mime=True, magic_file=data_file("win32", "magic.mgc")
    )

def from_file(*args, **kwargs):
    if not supported:
        return ""

    patch()
    return magic.from_file(*args, **kwargs)

def from_buffer(*args, **kwargs):
    if not supported:
        return ""

    patch()
    return magic.from_buffer(*args, **kwargs)

