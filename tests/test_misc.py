# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import zipfile

from sflock.misc import ZipCrypt, zip_set_password, make_list

def test_zipdecryptor_decrypt():
    a, b = zipfile._ZipDecrypter("password"), ZipCrypt("password")
    s1 = "".join(a(ch) for ch in "foobar")
    s2 = "".join(b.decrypt(ch) for ch in "foobar")
    assert s1 == s2

def test_zipdecryptor_encrypt():
    a, b = zipfile._ZipDecrypter("password"), ZipCrypt("password")
    assert "".join(a(b.encrypt(ch)) for ch in "barfoo") == "barfoo"

def test_zip_passwd():
    r = io.BytesIO()
    z = zipfile.ZipFile(r, "w")

    z.writestr("a.txt", "hello world")
    z.writestr("b.txt", "A"*1024)

    value = zip_set_password(z, "password")
    z.close()

    z = zipfile.ZipFile(io.BytesIO(value))
    z.setpassword("password")
    assert z.read("a.txt") == "hello world"
    assert z.read("b.txt") == "A"*1024

def test_make_list():
    assert make_list(None) == [None]
    assert make_list([]) == []
    assert make_list(()) == []
    assert make_list(1) == [1]
    assert make_list("a") == ["a"]
    assert make_list((1, 2)) == [1, 2]
    assert make_list([3, 4]) == [3, 4]
