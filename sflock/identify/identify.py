from sflock.abstracts import Identifier
import re

class Wsf(Identifier):
    name = "Wsf"
    ext = ["wsf"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        match = re.search(
            b"<script\\s+language=\"(J|VB|Perl)Script\"", f.contents, re.I
        )
        if match:
            return Wsf.name, Wsf.ext, Wsf.platform

class PS1(Identifier):
    name = "Powershell"
    ext = [".ps1"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        POWERSHELL_STRS = [
            b"$PSHOME", b"Get-WmiObject", b"Write-", b"new-object",
            b"Start-Process", b"Copy-Item", b"Set-ItemProperty",
            b"Select-Object"
        ]

        found = 0
        for s in POWERSHELL_STRS:
            if s in f.contents:
                found += 1

        if found > 1:
            return PS1.name, PS1.ext, PS1.platform

class Msi(Identifier):
    name = "Msi"
    ext = [".msi"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "Composite Document File V2 Document" in f.magic and "SAT" in f.magic:
            return Msi.name, Msi.ext, Msi.platform

class Jse(Identifier):
    name = "Jse"
    ext = [".jse"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        filename = f.filename if f.filename else ""
        if filename.lower().endswith("jse"):
            return Jse.name, Jse.ext, Jse.platform

class Vbs(Identifier):
    name = "VB script"
    ext = ["vb"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        VB_STRS = [
            b"Dim ", b"Set ", b"Attribute ", b"Public ",
            b"#If", b"#Else", b"#End If", b"End Function",
            b"End Sub", b"VBA", b"MsgBox "
        ]

        found = 0
        for s in VB_STRS:
            if s in f.contents:
                found += 1

        if found > 5:
            return Vbs.name, Vbs.ext, Vbs.platform

class Hta(Identifier):
    name = "HTML file type"
    ext = ["html"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "HTML document" in f.magic:
            return Hta.name, Hta.ext, Hta.platform

class Jar(Identifier):
    name = "Java archive data"
    ext = ["jar"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "JAR" in f.magic:
            return Jar.name, Jar.ext, Jar.platform

class Ppt(Identifier):
    name = "PowerPoint document"
    ext = ["ppt"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "Composite Document File V2 Document" in f.magic and "powerpoint" in f.mime:
            return Ppt.name, Ppt.ext, Ppt.platform

class Excel(Identifier):
    name = "Excel document"
    ext = ["xls", "xlsx"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        filename = f.filename if f.filename else ""
        if filename.lower().endswith(tuple(Excel.ext)):
            return Excel.name, Excel.ext, Excel.platform

        if "Composite Document File V2 Document" in f.magic and "excel" in f.mime:
            return


class Doc(Identifier):
    name = "Word document"
    ext = ["doc"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "Composite Document File V2 Document" in f.magic and "msword" in f.mime:
            return Doc.name, Doc.ext, Doc.platform

class Hwp(Identifier):
    name = "Hangul (Korean) Word Processor"
    ext = ["hwp"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "Hangul (Korean) Word Processor" in f.magic:
            return Hwp.name, Hwp.ext, Hwp.platform

class Pub(Identifier):
    name = "Microsoft Publisher"
    ext = ["pub"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        filename = f.filename if f.filename else ""
        if filename.lower().endswith(".pub"):
            return Pub.name, Pub.ext, Pub.platform

class Pdf(Identifier):
    name = "pdf"
    ext = ["pdf"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "PDF" in f.magic:
            return Pdf.name, Pdf.ext, Pdf.platform

class Exe(Identifier):
    name = "executable"
    ext = ["exe"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "PE32" in f.magic or "MS-DOS" in f.magic:
            return Exe.name, Exe.ext, Exe.platform

class Dll(Identifier):
    name = "dynamic-link library"
    ext = ["dll"]
    platform = ["windows"]

    @staticmethod
    def identify(f):
        if "DLL" in f.magic:
            filename = f.filename if f.filename else ""

            if filename.lower().endswith(".cpl"):
                return "cpl", ["cpl"], Dll.platform
            return Dll.name, Dll.ext, Dll.platform

class Python(Identifier):
    name = "python"
    ext = ["py"]
    platform = ["windows", "linux", "mac"]

    @staticmethod
    def identify(f):
        if "Python script" in f.magic:
            return Python.name, Python.ext, Python.platform

class Javascript(Identifier):
    name = "javascript"
    ext = ["js"]
    platform = ["windows", "linux", "mac"]

    @staticmethod
    def identify(f):
        JS_STRS = [
            b"var ", b"function ", b"eval", b" true",
            b" false", b" null", b"Math.", b"alert("
        ]

        found = 0
        for s in JS_STRS:
            if s in f.contents:
                found += 1

        if found > 5:
            return Javascript.name, Javascript.ext, Javascript.platform
