# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.
import os

doc_hdr = (b"\x7b\x5c\x72\x74",)
suffix_dic = {
    b".jar": "jar",
    b".py": "python",
    b".pyc": "python",
    b".pyo": "python",
    b".vbs": "vbs",
    b".js": "js",
    b".jse": "jse",
    b".msi": "msi",
    b".ps1": "ps1",
    b".ps1xml": "ps1",
    b".psc1": "ps1",
    b".psm1": "ps1",
    b".wsf": "wsf",
    b".wsc": "wsf",
    b".lnk": "generic",
    b".bat": "generic",
    b".cmd": "generic",
    b".htm": "ie",
    b".html": "ie",
    b".hta": "ie",
    b".mht": "ie",
    b".mhtml": "ie",
    b".url": "ie",
    b".ppt": "ppt",
    b".pptx": "ppt",
    b".pps": "ppt",
    b".ppsx": "ppt",
    b".pptm": "ppt",
    b".potm": "ppt",
    b".potx": "ppt",
    b".ppsm": "ppt",
    b".pot": "ppt",
    b".ppam": "ppt",
    b".sldx": "ppt",
    b".sldm": "ppt",
    b".xls": "xls",
    b".xlsx": "xls",
    b".xlm": "xls",
    b".xlt": "xls",
    b".xltx": "xls",
    b".xlsm": "xls",
    b".xltm": "xls",
    b".xlsb": "xls",
    b".xla": "xls",
    b".xlam": "xls",
    b".xll": "xls",
    b".xlw": "xls",
    b".slk": "xls",
    b".iqy": "xls",
    b".rtf": "doc",
    b".doc": "doc",
    b".docx": "doc",
    b".docm": "doc",
    b".dot": "doc",
    b".dotx": "doc",
    b".docb": "doc",
    b".mso": "doc",
    b".pdf": "pdf",
    b".pub": "pub",
}
eml_magics = (
    "RFC 822 mail",
    "old news",
    "mail forwarding",
    "smtp mail",
    "news",
    "news or mail",
    "saved news",
    "MIME entity",
)
jar_magics = (
    "Java Jar archive",
    "META-INF/MANIFEST.MF",
    "Java Jar file data (zip)",
    "Java archive data (JAR)",
)

  
def package(f):
    """Guesses the package based on the filename and/or contents."""
    filename = f.filename.lower() if f.filename else b""
    header = f.stream.read(0x1000)

    if "DLL" in f.magic:
        if filename.endswith(b".cpl"):
            return "cpl"
        # TODO Support PE exports to identify COM objects.
        return "dll"

    if "PE32" in f.magic or "MS-DOS" in f.magic:
        return "exe"

    if "PDF" in f.magic:
        return "pdf"
    
    if is_magic(f, eml_magics):
        return "eml"
    
    if is_magic(f, jar_magics):
        return "jar"
    
    if "HTML" in f.magic:
        return "ie"
    
    if "Python script" in f.magic:
        return "python"

    if "vbs" in f.magic:
        return "vbs"
    
    if "Zip archive" in f.magic:
        return "zip"
    
    if "RAR archive" in f.magic:
        return "rar"

    if "7-zip archive" in f.magic:
        return "7z"

    # TODO Get rid of this logic and replace it by actually inspecting
    # the contents of the .zip files (in case of Office 2007+).
    if "Rich Text Format" in f.magic or "Microsoft Word" in f.magic or "Microsoft Office Word" in f.magic:
        return "doc"

    if header.startswith(doc_hdr):
        return "doc"

    if "Microsoft Office Excel" in f.magic or "Microsoft Excel" in f.magic:
        return "xls"

    if "Microsoft PowerPoint" in f.magic:
        return "ppt"

    if "MS Windows shortcut" in f.magic:
        return "generic"
    
    package = use_suffix_for_package(filename, suffix_dic)
    if package:
        return package

    if is_bash_script(f) or is_elf_executable(f):
        return "generic"


def use_suffix_for_package(filename, suffix_dic):
    suffix = os.path.splitext(filename)[1]
    if suffix:
        return suffix_dic.get(suffix)


def is_bash_script(f):
    return f.filename and f.filename.endswith(b".sh")


def is_elf_executable(f):
    return f.magic.startswith("ELF")

def is_magic(f, type_magics):
    for magic in type_magics:
        if magic in f.magic:
            return True



platforms = {
    "cpl": "windows",
    "dll": "windows",
    "doc": "windows",
    "exe": "windows",
    "ie": "windows",
    "msi": "windows",
    "ppt": "windows",
    "ps1": "windows",
    "pub": "windows",
    "vbs": "windows",
    "wsf": "windows",
    "xls": "windows",
}


def platform(f):
    if f.package == "generic":
        if is_bash_script(f) or is_elf_executable(f):
            return "linux"
        else:
            return "windows"

    return platforms.get(f.package)
