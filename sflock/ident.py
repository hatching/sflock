# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import re

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
    if not f.get_child("[Content_Types].xml"):
        return

    # Shortcut for PowerPoint files.
    if f.get_child("ppt/presentation.xml"):
        return "ppt"

    if not f.get_child("docProps/app.xml"):
        return

    packages = {
        b"Microsoft Office Word": "doc",
        b"Microsoft Excel": "xls",
    }

    application = re.search(
        b"<application>(.*)</application>",
        f.read("docProps/app.xml"), re.I
    )
    if not application:
        return

    return packages.get(application.group(1))

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

def ruby(f):
    RB_STRS = [
        b"puts", b"END", b"START", b"require", b"ruby",
        b"end", b"load"
    ]

    found = 0
    for s in RB_STRS:
        if s in f.contents:
            found += 1

    if found > 3:
        return "rb"

def javascript(f):
    JS_STRS = [
        b"var ", b"function ", b"eval", b" true",
        b" false", b" null", b"Math.", b"alert("
    ]

    found = 0
    for s in JS_STRS:
        if s in f.contents:
            found += 1

    if found > 5:
        return "js"

def wsf(f):
    # @todo
    # handle this <script id="OIddGOjUGdfolHCdIGVfgOojC" language="VBScript">
    # currently doing it by .{0,256}, kind hacky
    match = re.search(
        b"<script.{0,256}\\s+language=[\"\'](J|VB|Perl)Script", f.contents, re.I
    )
    if match:
        return "wsf"

def visualbasic(f):
    VB_STRS = [
        b"Dim ", b"Set ", b"Attribute ", b"Public ",
        b"#If", b"#Else", b"#End If", b"End Function",
        b"End Sub", b"VBA", b"Execute(", b"End if", b"Else",
        b"Exit Function", b"Is Nothing"
    ]

    found = 0
    for s in VB_STRS:
        if s in f.contents:
            found += 1

    if found > 5:
        return "vbs"
    return

def java(f):
    if not f.get_child("Start.class") and not f.get_child("META-INF/MANIFEST.MF"):
        return
    if f.get_child("AndroidManifest.xml"):
        return
    return "jar"

def python(f):
    PY_STRS = [
        b"import os", b"import sys", b"import ", b"from ",
        b"():", b"def ", b"#", b"print(", b"sleep("
    ]

    found = 0
    for s in PY_STRS:
        if s in f.contents:
            found += 1

    if found > 5:
        return "py"

def batch(f):
    BC_STRS = [
        b"@echo", b"@setlocal ", b"@exit", b"set", b"@pause",
        b"@ECHO", b"@SETLOCAL ", b"@EXIT", b"SET", b"@PAUSE",
        b"REM", b":init", b":parse",
        b":main", b"goto ", b"shift"
    ]

    found = 0
    for s in BC_STRS:
        if s in f.contents:
            found += 1

    if found > 5:
        return "bc"