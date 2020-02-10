# Copyright (C) 2016-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

doc_ext = (
    ".rtf", ".doc", ".docx", ".docm", ".dot", ".dotx", ".docb",
    ".mso",
)
doc_hdr = (
    b"\x7b\x5c\x72\x74",
)
xls_ext = (
    ".xls", ".xlsx", ".xlm", ".xlt", ".xltx", ".xlsm", ".xltm",
    ".xlsb", ".xla", ".xlam", ".xll", ".xlw", ".slk", ".iqy",
)
ppt_ext = (
    ".ppt", ".pptx", ".pps", ".ppsx", ".pptm", ".potm", ".potx",
    ".ppsm", ".pot", ".ppam", ".sldx", ".sldm",
)
ie_ext = (
    ".htm", ".html", ".hta", ".mht", ".mhtml", ".url",
)

def package(f):
    """Guesses the package based on the filename and/or contents."""
    filename = f.filename.lower() if f.filename else ""
    header = f.stream.read(0x1000)

    if "DLL" in f.magic:
        if filename.endswith(".cpl"):
            return "cpl"
        # TODO Support PE exports to identify COM objects.
        return "dll"

    if "PE32" in f.magic or "MS-DOS" in f.magic:
        return "exe"

    if "PDF" in f.magic or filename.endswith(".pdf"):
        return "pdf"

    if filename.endswith(doc_ext):
        return "doc"

    if filename.endswith(xls_ext):
        return "xls"

    if filename.endswith(ppt_ext):
        return "ppt"

    if filename.endswith(".pub"):
        return "pub"

    # TODO Get rid of this logic and replace it by actually inspecting
    # the contents of the .zip files (in case of Office 2007+).
    if "Rich Text Format" in f.magic or \
            "Microsoft Word" in f.magic or \
            "Microsoft Office Word" in f.magic:
        return "doc"

    if header.startswith(doc_hdr):
        return "doc"

    if "Microsoft Office Excel" in f.magic or \
            "Microsoft Excel" in f.magic:
        return "xls"

    if "Microsoft PowerPoint" in f.magic:
        return "ppt"

    if filename.endswith(".jar"):
        return "jar"

    if filename.endswith((".py", ".pyc", ".pyo")):
        return "python"

    if "Python script" in f.magic:
        return "python"

    if filename.endswith(".vbs"):
        return "vbs"

    if filename.endswith(".js"):
        return "js"

    if filename.endswith(".jse"):
        return "jse"

    if filename.endswith(".msi"):
        return "msi"

    if filename.endswith((".ps1", ".ps1xml", ".psc1", ".psm1")):
        return "ps1"

    if filename.endswith((".wsf", ".wsc")):
        return "wsf"

    if filename.endswith(".lnk") or "MS Windows shortcut" in f.magic:
        return "generic"

    if filename.endswith((".bat", ".cmd")):
        return "generic"

    if "HTML" in f.magic or filename.endswith(ie_ext):
        return "ie"

    if is_bash_script(f) or is_elf_executable(f):
        return "generic"

def is_bash_script(f):
    return f.filename and f.filename.endswith(".sh")

def is_elf_executable(f):
    return f.magic.startswith("ELF")

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
