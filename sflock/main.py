# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from __future__ import print_function

import click
import glob
import io
import json
import os.path
import six
import zipfile

from sflock.abstracts import File, Unpacker
from sflock.exception import IncorrectUsageException
from sflock.ident import identify
from sflock.misc import make_list
from sflock.unpack import plugins

def supported():
    """Returns the supported extensions for this machine. Support for the
    unpacking of numerous file extensions depends on different system packages
    which should be installed on the machine."""
    ret = []
    for plugin in plugins.values():
        if plugin(None).supported():
            for ext in make_list(plugin.exts):
                ret.append(ext)
    return ret

def ident(f):
    """Identifies a file based on its contents."""
    package = identify(f)

    if package:
        f.preview = False
        f.package = package

        # Deselect the direct children.
        for child in f.children:
            child.selected = False
        return

    # Recursively enumerate further.
    for child in f.children:
        ident(child)

def unpack(filepath=None, contents=None, password=None, filename=None,
           duplicates=None):
    """Unpacks the file or contents provided."""
    if duplicates is None:
        duplicates = []

    if six.PY3:
        if isinstance(filepath, str) or isinstance(contents, str):
            raise IncorrectUsageException

        if isinstance(filename, str) or isinstance(password, str):
            raise IncorrectUsageException

    if contents:
        f = File(filepath, contents, filename=filename)
    else:
        f = File.from_path(filepath, filename=filename)

    Unpacker.single(f, password, duplicates)

    ident(f)
    return f

def zipify(f):
    """Turns any type of archive into an equivalent .zip file."""
    r = io.BytesIO()
    z = zipfile.ZipFile(r, "w")

    for child in f.children:
        filepath = child.temp_path()
        z.write(filepath, child.relapath.decode())
        os.unlink(filepath)

    z.close()
    return r.getvalue()

def process_file(filepath, extract):
    f = unpack(filepath)
    print(json.dumps(f.astree()))

    extract and f.extract(extract)

def process_directory(dirpath, extract):
    for rootpath, directories, filenames in os.walk(dirpath):
        for filename in filenames:
            process_file(os.path.join(rootpath, filename), extract)

@click.command()
@click.argument("files", nargs=-1)
@click.option("-e", "--extract", type=click.Path(file_okay=False))
def main(files, extract):
    for pattern in files:
        for path in glob.iglob(pattern):
            if os.path.isdir(path):
                process_directory(path, extract)
            else:
                process_file(path, extract)
