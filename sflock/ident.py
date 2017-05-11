# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import re

def office(f):
    if not f.get_child("[Content_Types].xml"):
        return

    if not f.get_child("docProps/app.xml"):
        return

    packages = {
        "Microsoft Office Word": "doc",
        "Microsoft Excel": "xls",
    }

    application = re.search(
        "<application>(.*)</application>",
        f.read("docProps/app.xml"), re.I
    )
    if not application:
        return

    return packages.get(application.group(1))

def identify(f):
    for identifier in identifiers:
        package = identifier(f)
        if package:
            return package

identifiers = [
    office,
]
