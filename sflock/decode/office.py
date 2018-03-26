# Copyright (C) 2017-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import base64
import hashlib
import struct
import xml.dom.minidom

# from Crypto.Cipher import PKCS1_v1_5
# from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from sflock.abstracts import Decoder, File

class EncryptedInfo(object):
    key_data_salt = None
    key_data_hash_alg = None
    verifier_hash_input = None
    verifier_hash_value = None
    encrypted_key_value = None
    spin_value = None
    password_salt = None
    password_hash_alg = None
    password_key_bits = None

class Office(Decoder):
    name = "office"

    def init(self):
        self.secret_key = None
        self.verifier_hash_input = None
        self.verifier_hash_value = None

    def get_hash(self, value, algorithm):
        if algorithm == "SHA512":
            return hashlib.sha512(value).digest()
        else:
            return hashlib.sha1(value).digest()

    def gen_encryption_key(self, block):
        if isinstance(self.password, bytes):
            self.password = self.password.decode()

        # Initial round sha512(salt + password).
        h = self.get_hash(
            self.ei.password_salt + str(self.password).encode("utf-16le"),
            self.ei.password_hash_alg
        )

        # Iteration of 0 -> spincount-1; hash = sha512(iterator + hash).
        for i in range(self.ei.spin_value):
            h = self.get_hash(
                struct.pack("<I", i) + h, self.ei.password_hash_alg
            )

        # Final skey and truncation.
        h = self.get_hash(h + block, self.ei.password_hash_alg)
        skey = h[:self.ei.password_key_bits // 8]
        return skey

    def init_secret_key(self):
        # TODO Add support for private keys.
        if False:
            # rsa = PKCS1_v1_5.new(RSA.importKey(self._private_key))
            # self.secret_key = rsa.decrypt(self.ei.encrypted_key_value, None)
            # Presumably the following is correct.
            # self.verifier_hash_input = rsa.decrypt(
                # self.ei.verifier_hash_input, None
            # )
            # self.verifier_hash_value = rsa.decrypt(
                # self.ei.verifier_hash_value, None
            # )
            pass

        if self.password:
            block_verifier_input = bytearray([
                0xfe, 0xa7, 0xd2, 0x76, 0x3b, 0x4b, 0x9e, 0x79
            ])
            block_verifier_value = bytearray([
                0xd7, 0xaa, 0x0f, 0x6d, 0x30, 0x61, 0x34, 0x4e
            ])
            block_encrypted_key = bytearray([
                0x14, 0x6e, 0x0b, 0xe7, 0xab, 0xac, 0xd0, 0xd6,
            ])

            # AES decrypt the encrypted* values with their pre-defined block
            # keys and salt in order to get secret key.
            aes = Cipher(
                algorithms.AES(self.gen_encryption_key(block_verifier_input)),
                modes.CBC(self.ei.password_salt),
                backend=default_backend()
            ).decryptor()
            self.verifier_hash_input = aes.update(
                self.ei.verifier_hash_input
            ) + aes.finalize()

            aes = Cipher(
                algorithms.AES(self.gen_encryption_key(block_verifier_value)),
                modes.CBC(self.ei.password_salt),
                backend=default_backend()
            ).decryptor()
            self.verifier_hash_value = aes.update(
                self.ei.verifier_hash_value
            ) + aes.finalize()

            aes = Cipher(
                algorithms.AES(self.gen_encryption_key(block_encrypted_key)),
                modes.CBC(self.ei.password_salt),
                backend=default_backend()
            ).decryptor()
            self.secret_key = (
                aes.update(self.ei.encrypted_key_value) + aes.finalize()
            )

    def decrypt_blob(self, f):
        ret = []
        # TODO Ensure that the assumption of "total size" being a 64-bit
        # integer is correct?
        for idx in range(0, struct.unpack("Q", f.read(8))[0], 0x1000):
            iv = self.get_hash(
                self.ei.key_data_salt + struct.pack("<I", idx),
                self.ei.key_data_hash_alg
            )
            aes = Cipher(
                algorithms.AES(self.secret_key),
                modes.CBC(iv[:16]),
                backend=default_backend()
            ).decryptor()
            ret.append(aes.update(f.read(0x1000)) + aes.finalize())
        return File(contents=b"".join(ret))

    def decode(self):
        if not self.f.ole:
            return

        if ["EncryptionInfo"] not in self.f.ole.listdir():
            return

        info = xml.dom.minidom.parseString(
            self.f.ole.openstream("EncryptionInfo").read()[8:]
        )
        key_data = info.getElementsByTagName("keyData")[0]
        password = info.getElementsByTagName("p:encryptedKey")[0]

        self.ei = ei = EncryptedInfo()
        ei.key_data_salt = base64.b64decode(
            key_data.getAttribute("saltValue")
        )
        ei.key_data_hash_alg = key_data.getAttribute("hashAlgorithm")
        ei.verifier_hash_input = base64.b64decode(
            password.getAttribute("encryptedVerifierHashInput")
        )
        ei.verifier_hash_value = base64.b64decode(
            password.getAttribute("encryptedVerifierHashValue")
        )
        ei.encrypted_key_value = base64.b64decode(
            password.getAttribute("encryptedKeyValue")
        )
        ei.spin_value = int(password.getAttribute("spinCount"))
        ei.password_salt = base64.b64decode(
            password.getAttribute("saltValue")
        )
        ei.password_hash_alg = password.getAttribute("hashAlgorithm")
        ei.password_key_bits = int(password.getAttribute("keyBits"))

        self.init_secret_key()

        verifier_hash = self.get_hash(
            self.verifier_hash_input, self.ei.password_hash_alg
        )
        # Incorrect password.
        if verifier_hash != self.verifier_hash_value:
            return False

        return self.decrypt_blob(self.f.ole.openstream("EncryptedPackage"))
