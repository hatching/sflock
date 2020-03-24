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
        return "Android Package File", "apk", ["android"]

    return "Java Archive File", "jar", ["windows"]

def OCTET(f):
    if f.contents.startswith(ttf_hdr):
        return "TrueType Font", "ttf", ["windows"]
    return "N64 Game ROM File", "rom", ["windows"]

matches = [
    # todo platform, add platform independent tag? for xml for example

    # Function, selected, magic, mime, extension, name, platform
    (False, False, "RPM", "rpm", "rpm", "Red Hat Package Manager File",
     ["linux"]),
    (False, False, "TIFF", "tiff", "tiff", "Tagged Image File Format",
     ["windows", "linux"]), # @todo, add android, ios, mac?
    (False, True, "Composite Document File V2 Document", "ms-excel", "xls",
     "Excel Spreadsheet", ["windows"]), # @todo, add android, ios, mac?
    (False, True, "RIFF", "x-wav", "wav", "WAVE Audio File", ["windows"]),
    (False, False, "XML", "xml", "xml", "XML File", ["windows"]),
    (False, False, "icon", "image/x-icon", "ico", "Icon File", ["windows"]),
    (False, False, "Apple HFS", "octet-stream", "ico", "Icon File",
     ["macOS"]),
    (False, True, "ISO Media", "video/mp4", "mp4", "MPEG-4 Video File",
     ["windows", "macOS"]),
    (False, False, "Debian binary package", "vnd.debian.binary-package", "deb",
     "Debian Software Package", ["linux"]),
    (False, False, "RealMedia file", "vnd.rn-realmedia", "rm",
     "RealMedia File", ["windows", "linux", "macOS"]),
    (False, False, "COM executable", "application", "com", "DOS Command File",
     ["windows"]),
    (False, False, "PNG", "png", "png", "Portable Network Graphic",
     ["windows"]),
    (False, True, "Python script", "x-python", "py", "Python Script",
     ["windows", "macOS", "linux"]),
    (False, False, "zlib", "zlib", "dmg", "Apple Disk Image", ["macOS"]),
    (False, True, "Composite Document File V2", "msword", "doc",
     "Microsoft Word Document", ["windows"]), # todo
    (False, True, "PDF", "pdf", "pdf", "Portable Document Format File",
     ["windows"]), # todo
    (False, True, "Macromedia Flash data", "x-shockwave-flash", "swf",
     "Shockwave Flash Movie", ["windows"]), # todo
    (False, True, "Composite Document File V2 Document", "ms-powerpoint",
     "ppt", "PowerPoint Presentation", ["windows"]), # todo
    (False, False, "Microsoft Cabinet archive data", "vnd.ms-cab", "cab",
     "Windows Cabinet File", ["windows"]),
    (False, True, "Composite Document File V2 Document", "msi", "msi",
     "Windows Installer Package", ["windows"]),
    (False, True, "MPEG", "mpeg", "mp3", "MP3 Audio File", ["windows"]), # todo
    (False, True, "RIFF", "msvideo", "avi", "Audio Video Interleave File",
     ["windows"]),
    (False, False, "JPEG", "jpeg", "jpg", "JPEG Image", ["windows"]), # todo
    (False, True, "Rich Text", "rtf", "rtf", "Rich Text Format File",
     ["windows"]),
    (False, True, "Macromedia Flash Video", "x-flv", "flv", "Flash Video File",
     ["windows"]), #todo
    (False, True, "Microsoft PowerPoint",
     "openxmlformats-officedocument.presentationml.presentation", "pptx",
     "PowerPoint Open XML Presentation", ["windows"]), #todo
    (False, False, "PostScript document", "postscript", "eps",
     "Encapsulated PostScript File", ["windows"]), #todo
    (False, True, "HTML", "html", "html", "Hypertext Markup Language File",
     ["windows"]), #todo
    (False, True, "PC bitmap", "x-ms-bmp", "bmp", "Bitmap Image File",
     ["windows"]),
    (False, True, "POSIX tar", "tar", "tar", "Consolidated Unix File Archive",
     ["linux"]),
    (False, False, "GIF image data", "gif", "gif",
     "Graphical Interchange Format File", ["windows"]), #todo
    (False, False, "MS Windows shortcut", "octet-stream", "lnk",
     "Windows Shortcut", ["windows"]),
    (False, True, "OpenDocument Text", "oasis.opendocument.text", "odt",
     "OpenDocument Text Document", ["windows"]), #todo
    (False, True, "OpenOffice", "octet-stream", "odt",
     "OpenDocument Text Document", ["windows"]), #todo
    (False, False, "Adobe Photoshop Image", "adobe.photoshop", "psd",
     "Adobe Photoshop Document", ["windows", "macOS"]),
    (False, False, "Microsoft ASF", "ms-asf", "asf",
     "Advanced Systems Format File", ["windows"]),
    (False, False, "3GPP", "octet-stream", "3gp", "3GPP Multimedia File",
     ["windows"]), #todo
    (False, False, "Google Chrome extension", "x-chrome-extension", "crx",
     "Chrome Extension", ["windows", "linux", "macOS"]),
    (False, False, "compiled Java class", "java-applet", "class",
     "Java Class File", ["windows", "macOS"]),
    (False, True, "RAR", "rar", "rar", "WinRAR Compressed Archive",
     ["windows"]),
    (False, False, "Hangul (Korean) Word Processor", "hwp", "hwp",
     "Hangul (Korean) Word Processor", ["windows"]), #todo
    (False, True, "Microsoft Word",
     "openxmlformats-officedocument.wordprocessingml.document", "docx",
     "Microsoft Word Open XML Document", ["windows"]), #todo
    (False, False, "PHP", "x-php", "php", "PHP Source Code File", ["windows"]), #todo
    (False, False, "Intel serial flash", "octet", "rom", "N64 Game ROM File",
     ["windows"]), # todo
    (False, True, "Microsoft Excel",
     "openxmlformats-officedocument.spreadsheetml.sheet", "xlsx",
     "Microsoft Excel Open XML Spreadsheet", ["windows"]), #todo
    (True, False, "Composite Document File V2 Document, Can't read SAT",
     "application/CDFV2", SAT),
    (True, False, "Composite Document File V2 Document, Cannot read section",
     "application/CDFV2", SECTION),
    # @todo should this be .torrent?
    (
    False, False, "BitTorrent", "x-bittorrent", "bittorrent", "Bittorent link",
    ["windows", "macOS"]),
    # todo
    (False, False, "SVG", "svg+xml", "svg", "Scalable vector graphics",
     ["windows"]),  # todo
    (
    False, True, "OpenDocument Spreadsheet", "opendocument.spreadsheet", "ods",
    "OpenDocument Spreadsheet", ["windows"]),  # todo
    (False, True, "OpenDocument", "opendocument.presentation", "odp",
     "OpenDocument Presentation", ["windows"]),  # todo
    (False, True, "compiled Java class", "x-java-applet", "class",
     "Java class file", ["windows"]),  # todo
    # (False, False, "data","octet-stream","ace","-",["widows"]),
    (False, True, "PE32", "x-dosexec", "exe", "Portable executable",
     ["windows"]),
    # (False, False, "data","octet-stream","mscompress","-",["windows"]),
    # @todo what should this be?
    (False, False, "MS Compress", "octet-stream", "mscompress",
     "Microsoft (de)compressor", ["windows"]),
    (False, False, "Python script", "x-python", "py", "Python script",
     ["windows", "linux"]),
    (False, False, "Bourne-Again shell", "x-shellscript", "sh", "Shell script",
     ["linux"]),
    (False, False, "GIMP XCF image", "x-xcf", "xcf", "GIMP XFC file",
     ["windows", "linux", "macOS"]),
    (False, False, "MIDI", "midi", "midi",
     "Musical Instrument Digital Interface", ["windows"]),
    (False, False, "MS-DOS", "x-dosexec", "mz", "DOS MZ executable ",
     ["windows"]),
    (False, False, "Macromedia Flash", "x-shockwave-flash", "flv",
     "Flash Video file", ["windows"]),
    # todo
    (False, False, "Perl script", "x-perl", "perl", "Perl script",
     ["windows", "linux"]),
    # todo
    # (False, False, "None","None","gul","-",["windows"]),
    (False, False, "Targa", "x-tga", "tga",
     "Truevision Graphics Adapter image file", ["windows", "macOS"]),  # todo
    (False, False, "Ogg", "ogg", "ogg", "Free open container format ",
     ["windows", "macOS"]),
    (False, False, "KGB", "octet-stream", "kgb", "Discontinued file archiver ",
     ["windows", "linux"]),
    (False, False, "ISO 9660", "x-iso9660-image", "iso", "ISO Image",
     ["windows"]),
    # (False, False, "data","octet-stream","machfs","-",["windows"]),
    # (False, False, "data","octet-stream","asd","-",["windows"]),
    (False, False, "Symbian", "x-sisx-app", "sis",
     "Software Installation Script", ["windows"]),
    (False, False, "iOS App", "x-ios-app", "ipa",
     "iOS application archive file", ["ios"]),
    (False, False, "AppleSingle", "octet-stream", "applesingle",
     "Mac File format", ["macOS"]),
    (False, False, "TeX font", "x-tex-tfm", "latex", "LaTeX file format",
     ["windows", "linux"]),  # todo
    (False, False, "bzip2", "x-bzip2", "bzip", "Compressed file", ["linux"]),
    (False, False, "AppleDouble", "octet-stream", "appledouble",
     "iOS application archive file", ["macOS"]),
    # http://fileformats.archiveteam.org/wiki/Mach-O
    (False, False, "Mach-O", "x-mach-binary", "macho",
     "File for executables, object code, shared libraries, dynamically-loaded"
     " code, and core dumps",
     ["macOS"]),
    (False, False, "ISO", "quicktime", "qt", "QuickTime file", ["macOS"]),
    (False, False, "text", "plain", "palmos", "OS for pda's or smarthpones",
     ["windows"]),  # todo
    # (False, False, "data","octet-stream","blackhole","-",["windows"]),
    # (False, False, "text","plain","c","C/C++ Source Code File",["windows"]),
    # (False, False, "None","None","jpeg","-",["windows"]),
    (False, False, "awk", "x-awk", "awk", "Script for text processing",
     ["linux"]),
    # (False, False, "data","octet-stream","emf","-",["windows"]),
    (False, False, "ARJ", "x-arj", "arj", "Compressed file archive",
     ["windows", "macOS"]),
    # (False, False, "data","octet-stream","dyalog","-",["windows"]),
    # (False, False, "data","octet-stream","coff","-",["windows"]),
    (False, False, "Apple binary property", "octet-stream", "apple",
     "Apple binary", ["macOS"]),
    (False, False, "Adobe InDesign", "octet-stream", "indd",
     "InDesign project file", ["windows"]),  # todo
    (False, False, "text", "plain", "ruby", "Ruby interpreted file",
     ["windows", "macOS", "linux"]),
    (False, False, "MPEG", "mpeg", "mpeg", "Compression for video and audio",
     ["windows"]),
    # (False, False, "None","None","fla","Adobe Animate Animation",["windows"]), #todo
    (False, False, "E-book", "octet-stream", "ebook", "Ebook file",
     ["windows"]),
    (False, False, "gzip", "gzip", "gz", "Compression file", ["windows"]),
    # todo
    (False, False, "text", "plain", "cookie", "Internet Explorer cookie",
     ["windows"]),
    (False, False, "ELF", "application", "elf", "Linux Executable", ["linux"]),
    (False, False, "Apple binary property", "octet-stream", "appleplist",
     "Apple binary", ["apple"]),
    (False, False, "MS-DOS", "x-dosexec", "exe", "Executable", ["windows"]),
    (False, False, "PE32", "x-dosexec", "dll", "Dynamic linked library",
     ["windows"]),
    (False, False, "FLAC", "x-flac", "flac", "Free lossless audio codec",
     ["windows"]),
    # todo
    (False, False, "SMTP", "rfc822", "email", "Email file", ["windows"]),
    (False, False, "FLC", "x-flc", "flc", "Animation file", ["macOS"]),
    # (False, False, "text","plain","text","-",["windows"]),
    # (False, False, "data","octet-stream","ttf","TrueType Font",["windows"]),
    (False, False, "ARC", "x-arc", "arc", "Compressed file",
     ["windows", "macOS"]),
    (False, False, "Dzip", "octet-stream", "dzip", "Witcher 2 game file",
     ["windows"]),
    (False, False, "7-zip", "x-7z-compressed", "7zip", "Compressed archive",
     ["windows"]),
    (
    False, False, "Python script", "x-python", "java", "Java Source Code File",
    ["windows"]),
    # (False, False, "text","plain","pascal","-",["windows"]),
    (False, False, "JNG", "x-jng", "jng", "Image file related to PNG",
     ["windows"]),
    (False, False, "capture", "tcpdump.pcap", "cap", "Network traffic data",
     ["windows"]),
    (False, False, "Mach-O", "x-mach-binary", "mac", "Bitmap graphic",
     ["macOS"]),
    (True, False, "text", "text", Text),
    (True, True, "Zip", "zip", ZIP),
    (True, True, "JAR", "java-archive", JAR),
    (True, False, "data", "octet", OCTET)
]


exttt = []
for i in matches:
    if i[0]:
        continue
    if i[4] in exttt:
        print(i[4])
    else:
        exttt.append(i[4])


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
