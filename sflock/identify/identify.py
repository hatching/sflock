from sflock.abstracts import Identifier

class Python(Identifier):
    name = "python"
    ext = [".py"]
    platform = ["windows", "linux", "mac"]

    @staticmethod
    def identify(f):
        if "Python script" in f.magic:
            return Python.name, Python.ext, Python.platform

class Javascript(Identifier):
    name = "javascript"
    ext = [".js"]
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
