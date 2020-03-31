from sflock.main import unpack
import os

pat = "/home/evert/tes"

def test_newident():
    for extension in os.listdir(pat):
        for sample in os.listdir(os.path.join(pat, extension)):
            f = unpack(contents=open(
                os.path.join(
                    pat, extension, sample
                ), "rb").read()
            )
            try:
                assert f.extension == extension
            except AssertionError:
                raise AssertionError(
                    "Sample: %s. Expected: %s, Received: %s" % (
                        sample, extension, f.extension
                    )
                )
