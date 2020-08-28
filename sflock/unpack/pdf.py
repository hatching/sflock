# Copyright (C) 2017-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os

import peepdf

from sflock.abstracts import Unpacker, File
from sflock.exception import UnpackException
from sflock.misc import make_list

class PdfFile(Unpacker):
    name = "pdffile"
    exts = ".pdf"
    package = "pdf"
    magic = "PDF document"

    def supported(self):
        return True

    def handles(self):

        # Temporarily only use the file magic to detect PDF files, as peepdf
        # can fail with invalid/fake PDFs.
        for magic in make_list(self.magic or []):
            if magic in self.f.magic:
                return True
        return False

    def unpack(self, depth=0, password=None, duplicates=None):
        entries = []

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        p = peepdf.PDFCore.PDFParser()

        try:
            _, f = p.parse(
                filepath, forceMode=True, looseMode=True, manualAnalysis=False
            )
        except Exception as e:
            raise UnpackException(f"peepdf parsing failure: {e}")


        for version in range(f.updates + 1):
            for obj in f.body[version].objects.values():
                if not isinstance(obj.object, peepdf.PDFCore.PDFDictionary):
                    continue

                el = obj.object.elements
                if "/F" not in el and "/UF" not in el:
                    continue
                if "/EF" not in el:
                    continue

                filename = el.get("/F") or el.get("/UF")
                if not isinstance(filename, peepdf.PDFCore.PDFString):
                    continue

                ref = el["/EF"]
                if not isinstance(ref, peepdf.PDFCore.PDFDictionary):
                    continue

                if "/F" not in ref.elements:
                    continue

                ref = ref.elements["/F"]
                if not isinstance(ref, peepdf.PDFCore.PDFReference):
                    continue

                if ref.id not in f.body[version].objects:
                    continue

                obj = f.body[version].objects[ref.id]
                contents = obj.object.decodedStream.encode("latin-1")
                filename = filename.value

                entries.append(File(
                    relapath=filename,
                    contents=contents,
                    filename=filename,
                    selected=False
                ))

        if temporary:
            os.unlink(filepath)

        return self.process(entries, duplicates, depth)
