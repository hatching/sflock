# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import re
from collections import OrderedDict

from sflock.aux.decode_vbe_jse import DecodeVBEJSE

try:
    from unicorn import Uc, UC_MODE_32, UC_MODE_64, UC_ARCH_X86, UC_HOOK_CODE, unicorn
    from unicorn.x86_const import UC_X86_REG_ESP
    HAVE_UNICORN = True
except ImportError:
    HAVE_UNICORN = False

file_extensions = OrderedDict(
    [
        ("msi", (b".msi", b".msp", b".appx")),
        ("pub", (b".pub",)),
        ("doc", (b".doc", b".dot", b".docx", b".dotx", b".docm", b".dotm", b".docb", b".rtf", b".mht", b".mso", b".wbk")),
        ("xls", (b".xls", b".xlt", b".xlm", b".xlsx", b".xltx", b".xlsm", b".xltm", b".xlsb", b".xla", b".xlam", b".xll", b".xlw", b".slk", b".xll", b".csv")),
        ("ppt", (b".ppt", b".ppa", b".pot", b".pps", b".pptx", b".pptm", b".potx", b".potm", b".ppam", b".ppsx", b".ppsm", b".sldx", b".sldm")),
        ("jar", (b".jar",)),
        # ("rar", (b".rar",)),
        ("reg", (b".reg",)),
        ("swf", (b".swf", b".fws")),
        ("python", (b".py", b".pyc", b".pyw")),
        ("ps1", (b".ps1",)),
        # ("msg", (b".msg",)),
        # ("eml", (b".eml", b".ics")),
        ("js", (b".js", b".jse")),
        ("ie", (b".html", b".url")), # b".htm",
        ("xps", (b".xps",)),
        ("hta", (b".hta",)),
        ("mht", (b".mht",)),
        ("lnk", (b".lnk",)),
        ("chm", (b".chm",)),
        ("hwp", (b".hwp", b".hwpx", b".hwt", b".hml")),
        ("inp", (b".inp", b".int")),
        ("xslt", (b".xsl", b".xslt")),
        ("wsf", (b".wsf",)),
        ("pdf", (b".pdf",)),
        ("vbs", (b".vbs", b".vbe")),
        ("msbuild", (b".csproj", b".vbproj", b".vcxproj", b".dbproj", b".fsproj")),
        ("zip", (b".zip",)),
        ("cpl", (b".cpl",)),
        ("ichitaro", (b".jtd", b".jtdc", b".jttc", b".jtt"))
    ]
)

mimes = OrderedDict(
    [
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
    ]
)

magics = OrderedDict(
    [
        # ToDo msdos
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
        ("Microsoft OOXML", "doc"),
        # ("MIME entity", "doc"),
        ("Microsoft Disk Image", "vhd"),
        ("PDF document", "pdf"),
        ("Windows imaging (WIM) image", "wim"),
        ("Nullsoft Installer", "nsis"),
        ("MSI Installer", "msi"),
        ("Java Jar", "jar"),
        ("Java archive", "jar"),
        ("RAR archive", "rar"),
        ("Macromedia Flash", "swf"),
        ("Python script", "python"),
        ("MS Windows 95 Internet shortcut", "html"),
        ("Windows URL shortcut", "html"),
        ("MS Windows shortcut", "lnk"),
        ("MS Windows HtmlHelp Data", "chm"),
        ("Hangul (Korean) Word Processor File", "hwp"),
        ("XSL stylesheet", "xslt"),
        # ("HTML", "html"),
    ]
)

shellcode_code_base = 0x100000
shellcode_threshold = 0x100
shellcode_limit = 0x100000


def detect_shellcode(f):
    global shellcode_count32, shellcode_count64, shellcode_last_address
    shellcode_count32 = 0
    shellcode_count64 = 0
    shellcode_last_address = 0
    emulate(f.contents, UC_MODE_64)
    if shellcode_last_address - shellcode_code_base < shellcode_threshold:
        shellcode_count64 = 0
    last_address = 0
    emulate(f.contents, UC_MODE_32)
    if last_address - shellcode_code_base < shellcode_threshold:
        shellcode_count32 = 0
    if shellcode_count64 > shellcode_threshold and shellcode_count64 > shellcode_count32:
        return "shellcode_64"
    elif shellcode_count32 > shellcode_threshold and shellcode_count32 > shellcode_count64:
        return "shellcode"
    return False

def hook_instr(uc, address, size, mode):
    global shellcode_count32, shellcode_count64, shellcode_last_address
    if mode == UC_MODE_32:
        shellcode_count32 += 1
    elif mode == UC_MODE_64:
        shellcode_count64 += 1
    shellcode_last_address = address

def emulate(data, mode):
    try:
        stack = 0x90000
        uc = Uc(UC_ARCH_X86, mode)
        uc.mem_map(stack, 0x1000*10)
        uc.mem_map(shellcode_code_base, 0x100000)
        uc.mem_write(shellcode_code_base, data)
        uc.reg_write(UC_X86_REG_ESP, stack+0x1000)
        uc.hook_add(UC_HOOK_CODE, hook_instr, user_data=mode)
        uc.emu_start(shellcode_code_base, shellcode_code_base+len(data), 0, shellcode_limit)
    except unicorn.UcError:
        pass

def inp(f):
    if b"InPage Arabic Document" in f.contents:
        return "inp"

def mso(f):
    if b"mso-application" in f.contents and b"Word.Document" in f.contents:
        return "doc"

def sct(f):
    if f.filename and f.filename.endswith(b".sct"):
        if re.search(br"(?is)<\?XML.*?<scriptlet.*?<registration", f.contents):
            return "sct"
        else:
            return "hta"

def xxe(f):
    STRINGS = [
        b"XXEncode",
        b"begin",
        b"+",
    ]

    found = 0
    for string in STRINGS:
        found += f.contents.count(string)

    if found >= 300 and b"XXEncode" in f.contents and b"begin" in f.contents:
        return "xxe"


def hta(f):
    STRINGS = [
        b"<head",
        b"<title",
        b"<body",
        b"SINGLEINSTANCE",
        b"<script",
        b"<input",
        b"WINDOWSTATE",
        b"APPLICATIONNAME",
        b"SCROLL",
        b"</",
    ]

    MANDATORY_STRINGS = [b"HTA:APPLICATION", b"<head", b"<body"]

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
        b"<o:Pages>",
        b"<o:DocumentProperties>",
        b"<o:Words>",
        b"<o:Characters>",
        b"<o:Lines>",
        b"<o:Paragraphs>",
        b"Content-Location:",
        b"Content-Transfer-Encoding:",
        b"Content-Type:",
        b"<o:OfficeDocumentSettings>",
    ]

    MANDATORY_STRINGS = [
        b"MIME-Version:",
        b"------=_NextPart_",
        b"<w:WordDocument>",
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

    if f.get_child(b"workbook.bin"):
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

    application = re.search(b"<application>(.*)</application>", f.read(b"docProps/app.xml"), re.I)
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
    if f.contents.startswith(b"MZ"):
        return None

    POWERSHELL_STRS = [
        b"$PSHOME",
        b"Get-WmiObject",
        b"Write-",
        b"new-object",
        b"Start-Process",
        b"Copy-Item",
        b"Set-ItemProperty",
        b"Select-Object",
        b"Set-StrictMode",
    ]

    found = 0
    for s in POWERSHELL_STRS:
        if s in f.contents:
            found += 1

    if found > 1:
        return "ps1"


def javascript(f):
    if f.contents.startswith(b"MZ"):
        return None

    JS_STRS = [
        b"var ",
        b"function ",
        b"eval",
        b" true",
        b" false",
        b" null",
        b"Math",
        b"alert(",
        b"charAt",
        b"decodeURIComponent",
        b"charCodeAt",
        b"toString",
    ]

    found = 0
    for s in JS_STRS:
        if s in f.contents:
            found += 1

    if found >= 5:
        return "js"


def wsf(f):
    match = re.search(b'<script\\s+language="(J|VB|Perl)Script"', f.contents, re.I)
    if match:
        return "wsf"


def pub(f):
    PUB_STRS = [
        b"Microsoft Publisher",
        b"MSPublisher",
    ]
    found = 0
    for s in PUB_STRS:
        if s in f.contents:
            found += 1

    if found >= 1:
        return "pub"


def visualbasic(f):
    if f.contents.startswith(b"MZ"):
        return None

    VB_STRS = [
        b"Dim ",
        b"dim ",
        b"Set ",
        b"Attribute ",
        b"Public ",
        b"If",
        b"Else",
        b"End If",
        b"End Function",
        b"End Sub",
        b"VBA",
        b"On Error",
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
    if any([child.magic == "AppleDouble encoded Macintosh file" for child in f.children or []]):
        return "dmg"


def vbe_jse(f):
    if b"#@~^" in f.contents[:100]:
        data = DecodeVBEJSE(f.contents, "")
        if data:
            if re.findall(b"\s?Dim\s", data, re.I):
                return "vbs"
            else:
                return "js"
        else:
            return "vbejse"


def identify(f):
    if not f.stream.read(0x1000):
        return

    if f.filename:
        for package, extensions in file_extensions.items():
            if f.filename.endswith(extensions):
                return package
    for identifier in identifiers:
        package = identifier(f)
        if package:
            return package
    for magic_types in magics:
        if f.magic.startswith(magic_types):
            return magics[magic_types]
    if f.mime in mimes:
        return mimes[f.mime]

    return detect_shellcode(f)


identifiers = [
    dmg,
    office_zip,
    office_ole,
    office_webarchive,
    office_activemime,
    hta,
    powershell,
    javascript,
    visualbasic,
    android,
    java,
    wsf,
    xxe,
    pub,
    vbe_jse,
    sct,
    inp,
]
