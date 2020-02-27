from sflock.abstracts import Identifier

class Python(Identifier):
    name = "python"
    ext = [".py"]
    platform = ["windows", "linux", "mac"]

    @staticmethod
    def identify(f):
        if "Python script" in f.magic:
            return Python.name, Python.ext, Python.platform
