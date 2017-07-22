# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import re

def hta(f):
    STRINGS = [
        "<head", "<title", "<body", "SINGLEINSTANCE",
        "<script", "<input", "WINDOWSTATE",
        "APPLICATIONNAME", "SCROLL", "</"
    ]

    MANDATORY_STRINGS = [
        "HTA:APPLICATION", "<head", "<body"
    ]

    # Make sure all mandatory strings are found
    for string in MANDATORY_STRINGS:
        if string not in f.contents:
            return

    found = 0
    for string in STRINGS:
        found += f.contents.count(string)

    if found >= 10:
        return "hta"

def office_webarchive(f):
    STRINGS = [
        "<o:Pages>", "<o:DocumentProperties>", "<o:Words>",
        "<o:Characters>", "<o:Lines>", "<o:Paragraphs>",
        "Content-Location:", "Content-Transfer-Encoding:",
        "Content-Type:", "<o:OfficeDocumentSettings>"
    ]

    MANDATORY_STRINGS = [
        "MIME-Version:", "------=_NextPart_", "<w:WordDocument>",
        "text/html",
    ]

    # Make sure all mandatory strings are found
    for string in MANDATORY_STRINGS:
        if string not in f.contents:
            return

    found = 0
    for string in STRINGS:
        found += f.contents.count(string)

    if found >= 10:
        return "doc"

def office_activemime(f):
    if f.contents.startswith('QWN0aXZlTWltZQ') or f.contents.startswith('ActiveMime'):
        return "doc"

def office_zip(f):
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

def office_ole(f):
    files = f.ole and f.ole.listdir() or []
    if ["WordDocument"] in files:
        return "doc"
    if ["Workbook"] in files:
        return "xls"

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
    office_zip, office_ole, office_webarchive, office_activemime,
    hta, powershell, javascript, visualbasic, android, java, wsf,
]
