ttf_hdr = (
    b'\x00\x01\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00'
)

def SAT(f):
    return None, None, None

def SECTION(f):
    return None, None, None

def Text(f):
    return None, None, None

def ZIP(f):
    return None, None, None

def JAR(f):
    if f.get_child("AndroidManifest.xml"):
        return "Android Package File", "apk", ["windows"]

    return "Java Archive File", "jar", ["windows"]

def OCTET(f):
    if f.contents.startswith(ttf_hdr):
        return "TrueType Font", "ttf", ["windows"]
    return "N64 Game ROM File", "rom", ["windows"]

matches = [
    # Function, selected, magic, mime, extension, name, platform
    (False, False, "RPM", "rpm", "rpm", "Red Hat Package Manager File",
     ["windows"]),
    (False, False, "TIFF", "tiff", "tiff", "Tagged Image File Format",
     ["windows"]),
    (False, True, "Composite Document File V2 Document", "ms-excel", "xls",
     "Excel Spreadsheet", ["windows"]),
    (False, True, "RIFF", "x-wav", "wav", "WAVE Audio File", ["windows"]),
    (False, False, "XML", "xml", "xml", "XML File", ["windows"]),
    (False, False, "icon", "image/x-icon", "ico", "Icon File", ["windows"]),
    (False, False, "Apple HFS", "octet-stream", "ico", "Icon File",
     ["windows"]),
    (False, True, "ISO Media", "video/mp4", "mp4", "MPEG-4 Video File",
     ["windows"]),
    (False, False, "Debian binary package", "vnd.debian.binary-package", "deb",
     "Debian Software Package", ["windows"]),
    (False, False, "RealMedia file", "vnd.rn-realmedia", "rm",
     "RealMedia File", ["windows"]),
    (False, False, "COM executable", "x-dosexec", "com", "DOS Command File",
     ["windows"]),
    (False, False, "PNG", "png", "png", "Portable Network Graphic",
     ["windows"]),
    (False, True, "Python script", "x-python", "py", "Python Script",
     ["windows"]),
    (False, False, "zlib", "zlib", "dmg", "Apple Disk Image", ["windows"]),
    (False, True, "Composite Document File V2", "msword", "doc",
     "Microsoft Word Document", ["windows"]),
    (False, True, "PDF", "pdf", "pdf", "Portable Document Format File",
     ["windows"]),
    (False, True, "Macromedia Flash data", "x-shockwave-flash", "swf",
     "Shockwave Flash Movie", ["windows"]),
    (False, True, "Composite Document File V2 Document", "ms-powerpoint",
     "ppt", "PowerPoint Presentation", ["windows"]),
    (False, False, "Microsoft Cabinet archive data", "vnd.ms-cab", "cab",
     "Windows Cabinet File", ["windows"]),
    (False, True, "Composite Document File V2 Document", "msi", "msi",
     "Windows Installer Package", ["windows"]),
    (False, True, "MPEG", "mpeg", "mp3", "MP3 Audio File", ["windows"]),
    (False, True, "RIFF", "msvideo", "avi", "Audio Video Interleave File",
     ["windows"]),
    (False, False, "JPEG", "jpeg", "jpg", "JPEG Image", ["windows"]),
    (False, True, "Rich Text", "rtf", "rtf", "Rich Text Format File",
     ["windows"]),
    (False, True, "Macromedia Flash Video", "x-flv", "flv", "Flash Video File",
     ["windows"]),
    (False, True, "Microsoft PowerPoint",
     "openxmlformats-officedocument.presentationml.presentation", "pptx",
     "PowerPoint Open XML Presentation", ["windows"]),
    (False, False, "PostScript document", "postscript", "eps",
     "Encapsulated PostScript File", ["windows"]),
    (False, True, "HTML", "html", "html", "Hypertext Markup Language File",
     ["windows"]),
    (False, True, "PC bitmap", "x-ms-bmp", "bmp", "Bitmap Image File",
     ["windows"]),
    (False, True, "POSIX tar", "tar", "tar", "Consolidated Unix File Archive",
     ["windows"]),
    (False, False, "GIF image data", "gif", "gif",
     "Graphical Interchange Format File", ["windows"]),
    (False, False, "MS Windows shortcut", "octet-stream", "lnk",
     "Windows Shortcut", ["windows"]),
    (False, True, "OpenDocument Text", "oasis.opendocument.text", "odt",
     "OpenDocument Text Document", ["windows"]),
    (False, True, "OpenOffice", "octet-stream", "odt",
     "OpenDocument Text Document", ["windows"]),
    (False, False, "Adobe Photoshop Image", "adobe.photoshop", "psd",
     "Adobe Photoshop Document", ["windows"]),
    (False, False, "Microsoft ASF", "ms-asf", "asf",
     "Advanced Systems Format File", ["windows"]),
    (False, False, "3GPP", "octet-stream", "3gp", "3GPP Multimedia File",
     ["windows"]),
    (False, False, "Google Chrome extension", "x-chrome-extension", "crx",
     "Chrome Extension", ["windows"]),
    (False, False, "compiled Java class", "java-applet", "class",
     "Java Class File", ["windows"]),
    (False, True, "RAR", "rar", "rar", "WinRAR Compressed Archive",
     ["windows"]),
    (False, False, "Hangul (Korean) Word Processor", "hwp", "hwp",
     "Hangul (Korean) Word Processor", ["windows"]),
    (False, True, "Microsoft Word",
     "openxmlformats-officedocument.wordprocessingml.document", "docx",
     "Microsoft Word Open XML Document", ["windows"]),
    (False, False, "PHP", "x-php", "php", "PHP Source Code File", ["windows"]),
    (False, False, "Intel serial flash", "octet", "rom", "N64 Game ROM File",
     ["windows"]),
    (False, True, "Microsoft Excel",
     "openxmlformats-officedocument.spreadsheetml.sheet", "xlsx",
     "Microsoft Excel Open XML Spreadsheet", ["windows"]),
    (True, False, "Composite Document File V2 Document, Can't read SAT",
     "application/CDFV2", SAT),
    (True, False, "Composite Document File V2 Document, Cannot read section",
     "application/CDFV2", SECTION),
    (True, False, "text", "text", Text),
    (True, True, "Zip", "zip", ZIP),
    (True, True, "JAR", "java-archive", JAR),
    (True, False, "data", "octet", OCTET)
]


def identify(f):
    # return: selected, name, extension, platform

    # Loop through every potential match
    for match in matches:
        function, selected, magic, mime = match[:4]
        # Check if it matches
        if magic in f.magic and mime in f.mime:
            # If the match is a function
            # Check if there is already a match found (on a non function match)
            # The non function matches are narrower
            if function:
                return (selected, *match[4](f))
            else:
                # @todo, decide what to do when multiple matches
                # For now, return
                return selected, match[5], match[4], match[6]
