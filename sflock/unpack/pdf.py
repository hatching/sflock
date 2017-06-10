# Copyright (C) 2017 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import peepdf

from sflock.abstracts import Unpacker, File

class PdfFile(Unpacker):
    name = "pdffile"
    exts = ".pdf"

    def supported(self):
        return True

    def unpack(self, password=None, duplicates=None):
        entries = []

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        p = peepdf.PDFCore.PDFParser()
        r, f = p.parse(
            filepath, forceMode=True,
            looseMode=True, manualAnalysis=False
        )
        if r:
            if temporary:
                os.unlink(filepath)
            return

        for version in xrange(f.updates + 1):
            for obj in f.body[version].objects.values():
                if not isinstance(obj.object, peepdf.PDFCore.PDFDictionary):
                    continue

                if "/F" not in obj.object.elements:
                    continue
                if "/EF" not in obj.object.elements:
                    continue

                filename = obj.object.elements["/F"]
                if not isinstance(filename, peepdf.PDFCore.PDFString):
                    continue

                ref = obj.object.elements["/EF"]
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
                entries.append(File(
                    contents=obj.object.decodedStream,
                    filename=filename.value,
                    selected=False
                ))

        if temporary:
            os.unlink(filepath)

        if entries:
            self.f.preview = False
        return self.process(entries, duplicates)
