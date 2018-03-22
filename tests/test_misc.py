# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import zipfile
import six
from sflock.misc import ZipCrypt, zip_set_password, make_list

def test_zipdecryptor_decrypt():
    a, b = zipfile._ZipDecrypter(b"password"), ZipCrypt(b"password")
    s1 = ""
    for ch in "foobar":
        if six.PY3:
            x = a(ord(ch))
            s1 += chr(x)
        else:
            x = a(ch)
            s1 += x
    s2 = ""
    for ch in "foobar":
        if six.PY3:
            x= b.decrypt(ord(ch))
            s2 += chr(x)
        else:
            x = b.decrypt(ch)
            s2 += x

    assert s1 == s2

def test_zipdecryptor_encrypt():
    a, b = zipfile._ZipDecrypter(b"password"), ZipCrypt(b"password")
    str = ""
    for ch in "barfoo":
        x = b.encrypt(ch)
        if six.PY3:
            y = a(ord(x))
            str += chr(y)
        else:
            y = a(x)
            str += y    
    assert str == "barfoo"
    #assert "".join(a() f   or ch in "barfoo") == "barfoo"

def test_zip_passwd():
    r = io.BytesIO()
    z = zipfile.ZipFile(r, "w")

    z.writestr("a.txt", "hello world")
    z.writestr("b.txt", "A"*1024)

    value = zip_set_password(z, b"password")
    z.close()
    #raise Exception(len(value))
    z = zipfile.ZipFile(io.BytesIO(value))
    z.setpassword(b"password")
    assert z.read("a.txt") == b"hello world"
    assert z.read("b.txt") == b"A"*1024

def test_make_list():
    assert make_list(None) == [None]
    assert make_list([]) == []
    assert make_list(()) == []
    assert make_list(1) == [1]
    assert make_list("a") == ["a"]
    assert make_list((1, 2)) == [1, 2]
    assert make_list([3, 4]) == [3, 4]
