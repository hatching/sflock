# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import importlib

def import_plugins(dirpath, module_prefix, namespace, class_):
    """Import plugins of type `class` located at `dirpath` into the
    `namespace` that starts with `module_prefix`. If `dirpath` represents a
    filepath then it is converted into its containing directory."""
    if os.path.isfile(dirpath):
        dirpath = os.path.dirname(dirpath)

    for fname in os.listdir(dirpath):
        if fname.endswith(".py") and not fname.startswith("__init__"):
            module_name, _ = os.path.splitext(fname)
            importlib.import_module("%s.%s" % (module_prefix, module_name))

    plugins = {}
    for subclass in class_.__subclasses__():
        namespace[subclass.__name__] = subclass
        plugins[subclass.__name__.lower()] = subclass
        class_.plugins[subclass.__name__.lower()] = subclass
    return plugins
