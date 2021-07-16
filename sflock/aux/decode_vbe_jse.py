#!/usr/bin/env python

__description__ = "Decode VBE/JSE script"
__author__ = "Didier Stevens"
__version__ = "0.0.1"
__date__ = "2016/03/28"

"""

Source code put in public domain by Didier Stevens, no Copyright
https://DidierStevens.com
Use at your own risk

History:
  2016/03/28: start

Todo:

Reference:
  https://gallery.technet.microsoft.com/Encode-and-Decode-a-VB-a480d74c
"""

import optparse
import sys
import os
import signal
import textwrap
import re


def PrintManual():
    manual = """
Manual:

This program reads from the given file or standard input, and converts the encoded VBE script to VBS.

"""
    for line in manual.split("\n"):
        print(textwrap.fill(line))


def File2String(filename):
    try:
        f = open(filename, "rb")
    except:
        return None
    try:
        return f.read()
    except:
        return None
    finally:
        f.close()


def FixPipe():
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except:
        pass


# Fix for http://bugs.python.org/issue11395
def StdoutWriteChunked(data):
    while data != "":
        # sys.stdout.write(data[0:10000])
        # sys.stdout.flush()
        data = data[10000:]


def Decode(data):
    dDecode = {}
    dDecode[9] = b"\x57\x6E\x7B"
    dDecode[10] = b"\x4A\x4C\x41"
    dDecode[11] = b"\x0B\x0B\x0B"
    dDecode[12] = b"\x0C\x0C\x0C"
    dDecode[13] = b"\x4A\x4C\x41"
    dDecode[14] = b"\x0E\x0E\x0E"
    dDecode[15] = b"\x0F\x0F\x0F"
    dDecode[16] = b"\x10\x10\x10"
    dDecode[17] = b"\x11\x11\x11"
    dDecode[18] = b"\x12\x12\x12"
    dDecode[19] = b"\x13\x13\x13"
    dDecode[20] = b"\x14\x14\x14"
    dDecode[21] = b"\x15\x15\x15"
    dDecode[22] = b"\x16\x16\x16"
    dDecode[23] = b"\x17\x17\x17"
    dDecode[24] = b"\x18\x18\x18"
    dDecode[25] = b"\x19\x19\x19"
    dDecode[26] = b"\x1A\x1A\x1A"
    dDecode[27] = b"\x1B\x1B\x1B"
    dDecode[28] = b"\x1C\x1C\x1C"
    dDecode[29] = b"\x1D\x1D\x1D"
    dDecode[30] = b"\x1E\x1E\x1E"
    dDecode[31] = b"\x1F\x1F\x1F"
    dDecode[32] = b"\x2E\x2D\x32"
    dDecode[33] = b"\x47\x75\x30"
    dDecode[34] = b"\x7A\x52\x21"
    dDecode[35] = b"\x56\x60\x29"
    dDecode[36] = b"\x42\x71\x5B"
    dDecode[37] = b"\x6A\x5E\x38"
    dDecode[38] = b"\x2F\x49\x33"
    dDecode[39] = b"\x26\x5C\x3D"
    dDecode[40] = b"\x49\x62\x58"
    dDecode[41] = b"\x41\x7D\x3A"
    dDecode[42] = b"\x34\x29\x35"
    dDecode[43] = b"\x32\x36\x65"
    dDecode[44] = b"\x5B\x20\x39"
    dDecode[45] = b"\x76\x7C\x5C"
    dDecode[46] = b"\x72\x7A\x56"
    dDecode[47] = b"\x43\x7F\x73"
    dDecode[48] = b"\x38\x6B\x66"
    dDecode[49] = b"\x39\x63\x4E"
    dDecode[50] = b"\x70\x33\x45"
    dDecode[51] = b"\x45\x2B\x6B"
    dDecode[52] = b"\x68\x68\x62"
    dDecode[53] = b"\x71\x51\x59"
    dDecode[54] = b"\x4F\x66\x78"
    dDecode[55] = b"\x09\x76\x5E"
    dDecode[56] = b"\x62\x31\x7D"
    dDecode[57] = b"\x44\x64\x4A"
    dDecode[58] = b"\x23\x54\x6D"
    dDecode[59] = b"\x75\x43\x71"
    dDecode[60] = b"\x4A\x4C\x41"
    dDecode[61] = b"\x7E\x3A\x60"
    dDecode[62] = b"\x4A\x4C\x41"
    dDecode[63] = b"\x5E\x7E\x53"
    dDecode[64] = b"\x40\x4C\x40"
    dDecode[65] = b"\x77\x45\x42"
    dDecode[66] = b"\x4A\x2C\x27"
    dDecode[67] = b"\x61\x2A\x48"
    dDecode[68] = b"\x5D\x74\x72"
    dDecode[69] = b"\x22\x27\x75"
    dDecode[70] = b"\x4B\x37\x31"
    dDecode[71] = b"\x6F\x44\x37"
    dDecode[72] = b"\x4E\x79\x4D"
    dDecode[73] = b"\x3B\x59\x52"
    dDecode[74] = b"\x4C\x2F\x22"
    dDecode[75] = b"\x50\x6F\x54"
    dDecode[76] = b"\x67\x26\x6A"
    dDecode[77] = b"\x2A\x72\x47"
    dDecode[78] = b"\x7D\x6A\x64"
    dDecode[79] = b"\x74\x39\x2D"
    dDecode[80] = b"\x54\x7B\x20"
    dDecode[81] = b"\x2B\x3F\x7F"
    dDecode[82] = b"\x2D\x38\x2E"
    dDecode[83] = b"\x2C\x77\x4C"
    dDecode[84] = b"\x30\x67\x5D"
    dDecode[85] = b"\x6E\x53\x7E"
    dDecode[86] = b"\x6B\x47\x6C"
    dDecode[87] = b"\x66\x34\x6F"
    dDecode[88] = b"\x35\x78\x79"
    dDecode[89] = b"\x25\x5D\x74"
    dDecode[90] = b"\x21\x30\x43"
    dDecode[91] = b"\x64\x23\x26"
    dDecode[92] = b"\x4D\x5A\x76"
    dDecode[93] = b"\x52\x5B\x25"
    dDecode[94] = b"\x63\x6C\x24"
    dDecode[95] = b"\x3F\x48\x2B"
    dDecode[96] = b"\x7B\x55\x28"
    dDecode[97] = b"\x78\x70\x23"
    dDecode[98] = b"\x29\x69\x41"
    dDecode[99] = b"\x28\x2E\x34"
    dDecode[100] = b"\x73\x4C\x09"
    dDecode[101] = b"\x59\x21\x2A"
    dDecode[102] = b"\x33\x24\x44"
    dDecode[103] = b"\x7F\x4E\x3F"
    dDecode[104] = b"\x6D\x50\x77"
    dDecode[105] = b"\x55\x09\x3B"
    dDecode[106] = b"\x53\x56\x55"
    dDecode[107] = b"\x7C\x73\x69"
    dDecode[108] = b"\x3A\x35\x61"
    dDecode[109] = b"\x5F\x61\x63"
    dDecode[110] = b"\x65\x4B\x50"
    dDecode[111] = b"\x46\x58\x67"
    dDecode[112] = b"\x58\x3B\x51"
    dDecode[113] = b"\x31\x57\x49"
    dDecode[114] = b"\x69\x22\x4F"
    dDecode[115] = b"\x6C\x6D\x46"
    dDecode[116] = b"\x5A\x4D\x68"
    dDecode[117] = b"\x48\x25\x7C"
    dDecode[118] = b"\x27\x28\x36"
    dDecode[119] = b"\x5C\x46\x70"
    dDecode[120] = b"\x3D\x4A\x6E"
    dDecode[121] = b"\x24\x32\x7A"
    dDecode[122] = b"\x79\x41\x2F"
    dDecode[123] = b"\x37\x3D\x5F"
    dDecode[124] = b"\x60\x5F\x4B"
    dDecode[125] = b"\x51\x4F\x5A"
    dDecode[126] = b"\x20\x42\x2C"
    dDecode[127] = b"\x36\x65\x57"

    dCombination = {}
    dCombination[0] = 0
    dCombination[1] = 1
    dCombination[2] = 2
    dCombination[3] = 0
    dCombination[4] = 1
    dCombination[5] = 2
    dCombination[6] = 1
    dCombination[7] = 2
    dCombination[8] = 2
    dCombination[9] = 1
    dCombination[10] = 2
    dCombination[11] = 1
    dCombination[12] = 0
    dCombination[13] = 2
    dCombination[14] = 1
    dCombination[15] = 2
    dCombination[16] = 0
    dCombination[17] = 2
    dCombination[18] = 1
    dCombination[19] = 2
    dCombination[20] = 0
    dCombination[21] = 0
    dCombination[22] = 1
    dCombination[23] = 2
    dCombination[24] = 2
    dCombination[25] = 1
    dCombination[26] = 0
    dCombination[27] = 2
    dCombination[28] = 1
    dCombination[29] = 2
    dCombination[30] = 2
    dCombination[31] = 1
    dCombination[32] = 0
    dCombination[33] = 0
    dCombination[34] = 2
    dCombination[35] = 1
    dCombination[36] = 2
    dCombination[37] = 1
    dCombination[38] = 2
    dCombination[39] = 0
    dCombination[40] = 2
    dCombination[41] = 0
    dCombination[42] = 0
    dCombination[43] = 1
    dCombination[44] = 2
    dCombination[45] = 0
    dCombination[46] = 2
    dCombination[47] = 1
    dCombination[48] = 0
    dCombination[49] = 2
    dCombination[50] = 1
    dCombination[51] = 2
    dCombination[52] = 0
    dCombination[53] = 0
    dCombination[54] = 1
    dCombination[55] = 2
    dCombination[56] = 2
    dCombination[57] = 0
    dCombination[58] = 0
    dCombination[59] = 1
    dCombination[60] = 2
    dCombination[61] = 0
    dCombination[62] = 2
    dCombination[63] = 1

    result = bytes()
    index = -1
    for char in (
        data.replace(b"@&", bytes([10])).replace(b"@#", bytes([13])).replace(b"@*", b">").replace(b"@!", b"<").replace(b"@$", b"@")
    ):
        if sys.version_info[0] == 3:
            byte = char
        else:
            byte = ord(char)
        if byte < 128:
            index = index + 1
        if (byte == 9 or byte > 31 and byte < 128) and byte != 60 and byte != 62 and byte != 64:
            char = [c for c in dDecode[byte]][dCombination[index % 64]]

        result += bytes([char])

    return result


def DecodeVBEJSE(content, options):
    FixPipe()
    if sys.platform == "win32":
        import msvcrt

        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    if content == "":
        content = sys.stdin.read()
    # else:
    #    content = File2String(filename)
    oMatch = re.search(b"#@~\^......==(.+)......==\^#~@", content)
    if oMatch == None:
        print("No encoded script found!")
        return False
    else:
        return Decode(oMatch.groups()[0])


def Main():
    oParser = optparse.OptionParser(usage="usage: %prog [options] [file]\n" + __description__, version="%prog " + __version__)
    oParser.add_option("-m", "--man", action="store_true", default=False, help="Print manual")
    (options, args) = oParser.parse_args()

    if options.man:
        oParser.print_help()
        PrintManual()
        return

    if len(args) > 1:
        oParser.print_help()
        print("")
        print("  Source code put in the public domain by Didier Stevens, no Copyright")
        print("  Use at your own risk")
        print("  https://DidierStevens.com")
        return
    elif len(args) == 0:
        DecodeVBEJSE("", options)
    else:
        DecodeVBEJSE(args[0], options)


if __name__ == "__main__":
    Main()
