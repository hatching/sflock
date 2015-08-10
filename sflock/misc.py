# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import importlib

def import_plugins(dirpath, namespace, class_):
    """Import plugins of type `class` located at `dirpath` into a `namespace`.
    If `dirpath` represents a filepath then it is converted into its
    containing directory."""
    if os.path.isfile(dirpath):
        dirpath = os.path.dirname(dirpath)

    for fname in os.listdir(dirpath):
        if fname.endswith(".py") and not fname.startswith("__init__"):
            importlib.import_module("sflock.unpack.%s" % fname.rstrip(".py"))

    for subclass in class_.__subclasses__():
        namespace[subclass.__name__] = subclass
