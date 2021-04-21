# Copyright (C) 2017-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import sys
# import peepdf

from sflock.abstracts import Unpacker, File

class PdfFile(Unpacker):
    name = "pdffile"
    exts = b".pdf"
    package = "pdf"

    def supported(self):
        return False

    def unpack(self, password=None, duplicates=None):
        entries = []
        """
        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path()
            temporary = True

        p = peepdf.PDFCore.PDFParser()
        _, f = p.parse(
            filepath, forceMode=True, looseMode=True, manualAnalysis=False
        )

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
                contents = obj.object.decodedStream
                filename = filename.value

                if sys.version_info.major == 3:
                    contents = contents.encode("latin-1")
                    filename = filename.encode()

                entries.append(File(
                    contents=contents,
                    filename=filename,
                    selected=False
                ))

        if temporary:
            os.unlink(filepath)
        if entries:
            self.f.preview = False
        """
        return self.process(entries, duplicates)

