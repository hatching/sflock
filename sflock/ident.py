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

def powershell(f):
    POWERSHELL_STRS = [
        b"$PSHOME", b"Get-WmiObject", b"Write-", b"new-object ",
        b"Start-Process", b"Copy-Item", b"Set-ItemProperty", b"Select-Object",
        b"New-Object ", b"Write-Error ", b"Write-Warning ", b"Invoke-Method ",
        b"Invoke-Expression ", b"Parameter(", b"Invoke-Item "
    ]

    found = 0
    for s in POWERSHELL_STRS:
        if s in f.contents:
            found += 1

    if found >= 2:
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
        b"function ", b"eval", b" true",
        b" false", b" null", b"Math.", b"alert(", b"typeof ",
        b"instanceof "
    ]

    found = 0
    for s in JS_STRS:
        if s in f.contents:
            found += 1

    varcount = f.contents.count(b"var ")
    if varcount >= 10:
        found += 3
    elif varcount >= 4:
        found += 2
    elif varcount > 0:
        found += 1

    if found >= 4:
        return "js"

def wsf(f):
    # Search for a <job id='something'> tag. Keep in mind the tag might be
    # something like '<  JoB     id=''>'. Limit the amount of whitespace to
    # match, otherwise it is unlimited.
    jobstart = re.search(
        rb"<[\s+]{0,1024}job[\s+]{0,1024}id=", f.contents, re.I
    )
    if not jobstart:
        return

    # The script should come after the job tag.
    # @todo
    # handle this <script id="OIddGOjUGdfolHCdIGVfgOojC" language="VBScript">
    # currently doing it by .{0,256}, kind hacky

    if re.compile(
            rb"<script.{0,256}\s+language=[\"\'](J|VB|Perl)Script", re.I
    ).search(f.contents, jobstart.end()):
        return "wsf"

    return

def visualbasic(f):
    VB_STRS = [
        b"Dim ", b"Set ", b"Attribute ", b"Public ",
        b"#If", b"#Else", b"#End If", b"End Function",
        b"End Sub", b"VBA", b"Execute(", b"End if", b"Else",
        b"Exit Function", b"Is Nothing", b"Loop ", b"Loop\n",
        b"Do Until ", b"Chr(", b"Function ", b"Sub ", b"ElseIf ", b"End Sub"
    ]

    found = 0
    for s in VB_STRS:
        if s in f.contents:
            found += 1

    if found >= 4:
        return "vbs"
    return

def java(f):
    if not f.get_child(r".*\.class$", regex=True) \
            and not f.get_child("META-INF/MANIFEST.MF"):
        return
    if f.get_child("AndroidManifest.xml"):
        return "apk"
    return "jar"

def python(f):
    PY_STRS = [
        b"():", b"def ", b"#", b"print(", b"sleep(", b"time.sleep(",
        b"ctypes", b"exec(", b"eval(", b"elif:", b"b64decode", b"os.", b"sys.",
        b"bytes(", b".encode("
    ]

    found = 0
    for s in PY_STRS:
        if s in f.contents:
            found += 1

    from_import = re.compile(rb"from[\s+]{1,5}[\S+]{1,50}[\s+]{1,5}import\s")
    direct_import = re.compile(rb"import[\s+]{1,5}[\S+]{1,50}")

    # Count from and import statements. Only regex search first X bytes of file
    limit = 1024 * 1024 * 2
    all_froms = len(from_import.findall(f.contents, 0, limit))
    all_directs = len(direct_import.findall(f.contents, 0, limit))

    if all_froms >= 4:
        found += 3
    elif all_froms > 0:
        found += 2

    if all_directs:
        if all_froms:
            # 'import' statements are part of 'from X import Y' statements.
            # Subtract their amount.
            all_directs -= all_froms

        if all_directs >= 4:
            found += 3
        elif all_directs > 0:
            found += 1

    if found >= 4:
        return "py"

def batch(f):
    BC_STRS = [
        b"@echo ", b"@setlocal ", b"@exit ", b"set ", b"@pause ",
        b":init", b":parse", b"goto ", b"schtasks ",
        b":main", b"shift", b"start ", b"taskkill ", b":: ",
        b"rem ", b"cls ", b"setlocal", b"exit ", b"sleep ", b"assoc ",
        b"xcopy ", b"copy ", b"ipconfig", b"attrib ", b"del ", b"call :"
    ]

    found = 0
    for s in BC_STRS:
        if re.search(s, f.contents, re.IGNORECASE):
            found += 1

    if found >= 5:
        return "bat"

def udf_token_search(f):
    """Tries to detect UDF filesystem.
    See https://wiki.osdev.org/UDF"""
    beaoffset = f.contents.find(b"BEA01")
    if beaoffset == -1:
        return False

    if f.contents.find(b"NSR02", beaoffset) != -1:
        return True

    if f.contents.find(b"NSR03", beaoffset) != -1:
        return True
