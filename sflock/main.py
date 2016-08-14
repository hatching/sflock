# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import click
import glob
import os.path

from sflock.abstracts import File
from sflock.unpack import plugins

def process_file(filepath):
    f = File.from_path(filepath)
    signature = f.get_signature()
    container = plugins[signature["unpacker"]](f)
    for entry in container.unpack(mode=signature["mode"]):
        print entry["file"].filepath

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
