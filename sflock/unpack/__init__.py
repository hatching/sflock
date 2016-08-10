# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import Unpacker
from sflock.misc import import_plugins

plugins = import_plugins(__file__, "sflock.unpack", globals(), Unpacker)
