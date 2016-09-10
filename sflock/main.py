# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import click
import glob
import io
import json
import os.path
import zipfile

from sflock.abstracts import File, Unpacker
from sflock.unpack import plugins

def supported():
    """Returns the supported extensions for this machine. Support for the
    unpacking of numerous file extensions depends on different system packages
    which should be installed on the machine."""
    ret = []
    for plugin in plugins.values():
        if plugin(None).supported():
            if isinstance(plugin.exts, basestring):
                ret.append(plugin.exts)
            else:
                ret.extend(plugin.exts)
    return ret

def unpack(filepath, contents=None, password=None):
    """Unpacks the file or contents provided."""
    if contents:
        f = File(filepath, contents)
    else:
        f = File.from_path(filepath)

    duplicates = []

    # Determine how we're going to unpack this file (if at all). It may not
    # have a file extension, e.g., when its filename is a hash. In those cases
    # we're going to take a look at the contents of the file.
    f.unpacker = Unpacker.guess(f)

    # Actually unpack any embedded files in this archive.
    if f.unpacker:
        plugin = plugins[f.unpacker](f)
        if plugin.supported():
            f.children = plugin.unpack(password, duplicates)

    return f

def zipify(f):
    """Turns any type of archive into an equivalent .zip file."""
    r = io.BytesIO()
    z = zipfile.ZipFile(r, "w")

    for child in f.children:
        z.writestr(child.relapath, child.contents)

    z.close()
    return r.getvalue()

def process_file(filepath):
    print json.dumps(unpack(filepath).astree())

def process_directory(dirpath):
    for rootpath, directories, filenames in os.walk(dirpath):
        for filename in filenames:
            process_file(os.path.join(rootpath, filename))

@click.command()
@click.argument("files", nargs=-1)
def main(files):
    for pattern in files:
        for path in glob.iglob(pattern):
            if os.path.isdir(path):
                process_directory(path)
            else:
                process_file(path)
