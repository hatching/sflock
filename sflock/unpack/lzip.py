import os
import shutil
import tempfile

from sflock.abstracts import Unpacker


class LzipFile(Unpacker):
    name = "lzip"
    exe = "/usr/bin/lzip"
    exts = b".lz"
    magic = "lzip compressed data, version: 1"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        file_name = os.path.basename(filepath)
        if type(file_name) is bytes:
            file_name = file_name.decode("utf-8")
        tmp_file = os.path.join(dirpath, file_name)
        shutil.copyfile(filepath, tmp_file)
        filepath = tmp_file
        # TEMP FIX? move to folder and check as ret will be empty
        # we don't use -o to preserve original filename
        ret = self.zipjail(filepath, dirpath, "-d", filepath)
        # ret will be empty due to
        # Blocked system call occurred during sandboxing!\nip=0x7f8e08e904fb sp=0x7ffe8e081698 abi=0 nr=93 syscall=fchown
        if not ret:
            files = os.listdir(dirpath)
            if files:
                os.remove(tmp_file)
                files.remove(os.path.basename(tmp_file))
            if not files:
                return []

        if temporary and os.path.exists(filepath):
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates, password)


"""
>>> from sflock import unpack
>>> q = unpack(b"test.lz")
(b'/usr/local/lib/python3.8/dist-packages/sflock/data/zipjail.elf', b'test.lz', b'', '-c=1', '--', '/usr/bin/lzip', '-d', b'test.lz')
b'' b'Blocked system call occurred during sandboxing!\nip=0x7f8e08e904fb sp=0x7ffe8e081698 abi=0 nr=93 syscall=fchown\n\x1b[1;34mKilling child 415983\x1b[0m\n' here
"""
