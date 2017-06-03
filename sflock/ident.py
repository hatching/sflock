# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import re

def office(f):
    if not f.get_child("[Content_Types].xml"):
        return

    # Shortcut for PowerPoint files.
    if f.get_child("ppt/presentation.xml"):
        return "ppt"

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

def powershell(f):
    POWERSHELL_STRS = [
        "$PSHOME", "Get-WmiObject", "Write-", "new-object",
        "Start-Process", "Copy-Item", "Set-ItemProperty"
    ]

    for s in POWERSHELL_STRS:
        if s in f.contents:
            return "ps1"

def javascript(f):
    JS_STRS = [
        "var ", "function ", "eval", " true",
        " false", " null", "Math.", "alert("
    ]

    found = 0
    for s in JS_STRS:
        if s in f.contents:
            found += 1

    if found > 5:
        return "js"

def wsf(f):
    match = re.search(
        "<script\\s+language=\"(J|VB|Perl)Script\"", f.contents, re.I
    )
    if match:
        return "wsf"

def visualbasic(f):
    VB_STRS = [
        "Dim ", "Set ", "Attribute ", "Public ",
        "#If", "#Else", "#End If", "End Function",
        "End Sub", "VBA"
    ]

    found = 0
    for s in VB_STRS:
        if s in f.contents:
            found += 1

    if found > 5:
        return "vbs"
    return

def java(f):
    if not f.get_child("META-INF/MANIFEST.MF"):
        return
    if f.get_child("AndroidManifest.xml"):
        return
    return "jar"

def android(f):
    if not f.get_child("AndroidManifest.xml"):
        return
    if not f.get_child("classes.dex"):
        return
    return "apk"

def identify(f):
    if not f.stream.read(0x1000):
        return

    for identifier in identifiers:
        package = identifier(f)
        if package:
            return package

identifiers = [
    office, powershell, javascript, visualbasic, android, java,
]
