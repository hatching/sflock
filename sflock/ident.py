# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import re
from collections import OrderedDict

from sflock.aux.decode_vbe_jse import DecodeVBEJSE

mimes = OrderedDict([
    ("application/x-lzh-compressed", "lzh"),
    ("application/x-iso9660-image", "iso"),
    ("application/zip", "zip"),
    ("application/gzip", "gzip"),
    ("text/x-python", "py"),
    ("application/x-rar", "rar"),
    ("application/x-7z-compressed", "7z"),
    ("application/x-bzip2", "bzip2"),
    ("application/x-tar", "tar"),
    ("application/java-archive", "jar"),
    ("application/x-dosexec", "exe"),
    ("application/vnd.ms-cab-compressed", "cab"),
    ("application/pdf", "pdf"),
])

magics = OrderedDict([
    ("ACE archive data", "ace"),
    ("PE32 executable (DLL)", "dll"),
    ("PE32+ executable (DLL)", "dll"),
    ("PE32 executable", "exe"),
    ("PE32+ executable", "exe"),
    ("Microsoft PowerPoint", "ppt"),
    ("Microsoft Office Excel", "xls"),
    ("Microsoft Excel", "xls"),
    ("Rich Text Format", "doc"),
    ("Microsoft Office Word", "doc"),
    ("Microsoft Word", "doc"),
    ("Microsoft Disk Image", "vhd"),
    ("PDF document", "pdf"),
    ("Windows imaging (WIM) image", "wim"),
])

def xxe(f):
    STRINGS = [
        b"XXEncode", b"begin", b"+",
    ]

    found = 0
    for string in STRINGS:
        found += f.contents.count(string)

    if found >= 300:
        return "xxe"

def hta(f):
    STRINGS = [
        b"<head", b"<title", b"<body", b"SINGLEINSTANCE",
        b"<script", b"<input", b"WINDOWSTATE",
        b"APPLICATIONNAME", b"SCROLL", b"</"
    ]

    MANDATORY_STRINGS = [
        b"HTA:APPLICATION", b"<head", b"<body"
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
        b"<o:Pages>", b"<o:DocumentProperties>", b"<o:Words>",
        b"<o:Characters>", b"<o:Lines>", b"<o:Paragraphs>",
        b"Content-Location:", b"Content-Transfer-Encoding:",
        b"Content-Type:", b"<o:OfficeDocumentSettings>"
    ]

    MANDATORY_STRINGS = [
        b"MIME-Version:", b"------=_NextPart_", b"<w:WordDocument>",
        b"text/html",
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
    if f.contents.startswith((b"QWN0aXZlTWltZQ", b"ActiveMime")):
        return "doc"

def office_zip(f):
    if not f.get_child(b"[Content_Types].xml"):
        return

    if f.get_child(b'workbook.bin'):
        return "xls"

    # Shortcut for PowerPoint files.
    if f.get_child(b"ppt/presentation.xml"):
        return "ppt"


    if not f.get_child(b"docProps/app.xml"):
        return

    packages = {
        b"Microsoft Office Word": "doc",
        b"Microsoft Excel": "xls",
    }

    application = re.search(
        b"<application>(.*)</application>",
        f.read(b"docProps/app.xml"), re.I
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
        b"$PSHOME", b"Get-WmiObject", b"Write-", b"new-object",
        b"Start-Process", b"Copy-Item", b"Set-ItemProperty", b"Select-Object"
    ]

    found = 0
    for s in POWERSHELL_STRS:
        if s in f.contents:
            found += 1

    if found > 1:
        return "ps1"

def javascript(f):
    JS_STRS = [
        b"var ", b"function ", b"eval", b" true",
        b" false", b" null", b"Math", b"alert(", b"charAt",
        b"decodeURIComponent", b"charCodeAt", b"toString",
    ]

    found = 0
    for s in JS_STRS:
        if s in f.contents:
            found += 1

    if found >= 5:
        return "js"

def wsf(f):
    match = re.search(
        b"<script\\s+language=\"(J|VB|Perl)Script\"", f.contents, re.I
    )
    if match:
        return "wsf"

def pub(f):
    PUB_STRS = [
        b"Microsoft Publisher", b"MSPublisher",
    ]
    found = 0
    for s in PUB_STRS:
        if s in f.contents:
            found += 1

    if found >= 1:
        return "pub"


def visualbasic(f):
    VB_STRS = [
        b"Dim ", b"dim ", b"Set ", b"Attribute ", b"Public ",
        b"If", b"Else", b"End If", b"End Function",
        b"End Sub", b"VBA", b"On Error"
    ]

    found = 0
    for s in VB_STRS:
        if s in f.contents:
            found += 1

    if found > 5:
        return "vbs"
    return

def java(f):
    if not f.get_child(b"META-INF/MANIFEST.MF"):
        return
    if f.get_child(b"AndroidManifest.xml"):
        return
    return "jar"

def android(f):
    if not f.get_child(b"AndroidManifest.xml"):
        return
    if not f.get_child(b"classes.dex"):
        return
    return "apk"

def dmg(f):
    if any([child.magic == 'AppleDouble encoded Macintosh file' for child in f.children or []]):
        return "dmg"

def vbe_jse(f):
    if b"#@~^" in f.contents[:100]:
        data = DecodeVBEJSE(f.contents, "")
        if data:
            if re.findall(b"\s?Dim\s", data, re.I):
                return "vbs"
            else:
                return "js"

def identify(f):
    if not f.stream.read(0x1000):
        return

    for identifier in identifiers:
        package = identifier(f)
        if package:
            return package
    for magic_types in magics:
        if f.magic.startswith(magic_types):
            return magics[magic_types]
    if f.mime in mimes:
        return mimes[f.mime]

identifiers = [
    dmg, office_zip, office_ole, office_webarchive, office_activemime,
    hta, powershell, javascript, visualbasic, android, java, wsf,
    xxe, pub, vbe_jse
]
