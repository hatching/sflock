# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

def package(f):
    """Guesses the package based on the filename and/or contents."""
    filename = f.filename.lower()

    if "DLL" in f.magic:
        if filename.endswith(".cpl"):
            return "cpl"
        # TODO Support PE exports to identify COM objects.
        return "dll"

    if "PE32" in f.magic or "MS-DOS" in f.magic:
        return "exe"

    if "PDF" in f.magic or filename.endswith(".pdf"):
        return "pdf"

    if filename.endswith((".rtf", ".doc", ".docx", ".docm", ".dot",
                          ".dotx", ".docb", ".mht", ".mso")):
        return "doc"

    if filename.endswith((".xls", ".xlsx", ".xlm", ".xlsx", ".xlt",
                          ".xltx", ".xlsm", ".xltm", ".xlsb", ".xla",
                          ".xlam", ".xll", ".xlw")):
        return "xls"

    if filename.endswith((".ppt", ".pptx", ".pps", ".ppsx", ".pptm",
                          ".potm", ".potx", ".ppsm", ".pot", ".ppam",
                          ".sldx", ".sldm")):
        return "ppt"

    if filename.endswith(".pub"):
        return "pub"

    # TODO Get rid of this logic and replace it by actually inspecting
    # the contents of the .zip files (in case of Office 2007+).
    if "Rich Text Format" in f.magic or \
            "Microsoft Word" in f.magic or \
            "Microsoft Office Word" in f.magic:
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

    if filename.endswith((".js", ".jse")):
        return "js"

    if filename.endswith(".msi"):
        return "msi"

    if filename.endswith((".ps1", ".ps1xml", ".psc1", ".psm1")):
        return "ps1"

    if filename.endswith(".wsf"):
        return "wsf"

    if "HTML" in f.magic or filename.endswith((".htm", ".html")):
        return "ie"
