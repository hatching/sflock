# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import importlib
import os
import zipfile

import sflock

def import_plugins(dirpath, module_prefix, namespace, class_):
    """Import plugins of type `class` located at `dirpath` into the
    `namespace` that starts with `module_prefix`. If `dirpath` represents a
    filepath then it is converted into its containing directory."""
    if os.path.isfile(dirpath):
        dirpath = os.path.dirname(dirpath)

    for fname in os.listdir(dirpath):
        if fname.endswith(".py") and not fname.startswith("__init__"):
            module_name, _ = os.path.splitext(fname)
            importlib.import_module("%s.%s" % (module_prefix, module_name))

    plugins = {}
    for subclass in class_.__subclasses__():
        namespace[subclass.__name__] = subclass
        plugins[subclass.name.lower()] = subclass
        class_.plugins[subclass.name.lower()] = subclass
    return plugins

def data_file(*path):
    """Return the path for the filepath of an embedded file."""
    return os.path.abspath(os.path.join(sflock.__path__[0], "data", *path))

class ZipCrypt(zipfile._ZipDecrypter):
    """Layer on top of zipfile's _ZipDecrypter class to also encrypt data."""

    def __init__(self, password):
        self.init = True
        zipfile._ZipDecrypter.__init__(self, password)
        self.init = False

    def _UpdateKeys(self, c):
        """Override _UpdateKeys method so that __call__ may be reused."""
        self.init and zipfile._ZipDecrypter._UpdateKeys(self, c)

    def decrypt(self, ch):
        """Decrypt one character."""
        ch = self.__call__(ch)
        zipfile._ZipDecrypter._UpdateKeys(self, ch)
        return ch

    def encrypt(self, ch):
        """Encrypt one character."""
        t = chr(ord(self.__call__(ch)) ^ ord(ch))
        zipfile._ZipDecrypter._UpdateKeys(self, ch)
        return chr(ord(ch) ^ ord(t))

class ZipInfoWithPassword(zipfile.ZipInfo):
    """Layer on top of zipfile's ZipFile to emit password protected files."""
    ZIP_FLAG_PASSWORD = 1

    def __init__(self, zi, password, buf):
        kw = {
            "CRC": "crc",
        }
        # Copy all ZipInfo attributes.
        for key in zi.__slots__:
            setattr(self, kw.get(key, key), getattr(zi, key, None))

        # TODO Handle check against the file type from extended local headers.
        assert (zi.flag_bits & 8) == 0

        # Initialize ZipInfo header for password encrypted files.
        self.pw_header = "A"*11 + chr(zi.CRC >> 24)
        self.flag_bits |= self.ZIP_FLAG_PASSWORD

        # Encrypted contents that may be written away as-is.
        c = ZipCrypt(password)
        self.contents = "".join(c.encrypt(ch) for ch in self.pw_header + buf)

    @property
    def CRC(self):
        return self.crc

    @CRC.setter
    def CRC(self, value):
        """ZipFile.writestr() will recalculate the CRC. We can't allow this as
        it will destroy the integrity of our file. Furthermore, the password
        header (the first twelve bytes - the part that we add) are not even
        part of the CRC, so in the end the CRC will actually remain correct."""

def zip_set_password(z, password):
    """Applies a password before writing a ZipFile to file. Note that the
    return value of this function should be used, *not* the first parameter."""
    out = io.BytesIO()
    r = zipfile.ZipFile(out, "w")

    for zi in z.infolist():
        zi = ZipInfoWithPassword(zi, password, z.read(zi))
        r.writestr(zi, zi.contents)

    r.close()
    return out.getvalue()
