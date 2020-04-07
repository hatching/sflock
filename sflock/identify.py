import re
from sflock.ident import javascript, powershell, wsf, visualbasic, office_webarchive
ttf_hdr = (
    b'\x00\x01\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00'
)

WINDOWS = "windows"
MACOS = "darwin"
LINUX = "linux"
ANDROID = "android"
IOS = "ios"

def XML(f):
    if b"application/vnd.openxmlformats-officedocument" in f.contents:
        return "Office file", "doc", (WINDOWS,)
    return None, None, None

def SAT(f):
    if f.get_child("ppt/presentation.xml"):
        return "Powerpoint", "ppt", (WINDOWS,)

    return None, None, None

def SECTION(f):
    return None, None, None

def Text(f):
    if javascript(f):
        return "Javascript file", "js", (WINDOWS,)
    if powershell(f):
        return "Powershell script", "ps1", (WINDOWS,)
    if wsf(f):
        return "Windows script file", "wsf", (WINDOWS,)
    if visualbasic(f):
        return "Visual basic file", "vb", (WINDOWS,)
    return None, None, None

def ZIP(f):
    for i in f.children:
        if i.filename.lower() == "workbook.xml":
            return "Excel document", "xlsx", (WINDOWS,)
        if i.filename.lower() == "worddocument.xml":
            return "Word document", "docx", (WINDOWS,)
    return None, None, None

def JAR(f):
    if f.get_child("AndroidManifest.xml"):
        return "Android Package File", "apk", (ANDROID,)

    return "Java Archive File", "jar", (WINDOWS,)

def OCTET(f):
    if f.contents.startswith(ttf_hdr):
        return "TrueType Font", "ttf", (WINDOWS,)
    return "N64 Game ROM File", "rom", (WINDOWS,)

matches = [
    # todo platform, add platform independent tag? for xml for example

    # Function, selected, magic, mime, extension, name, platform
    (False, False, "RPM", "rpm", "rpm", "Red Hat Package Manager File",
     (LINUX,)),
    (False, False, "TIFF", "tiff", "tiff", "Tagged Image File Format",
     (WINDOWS, LINUX)), # @todo, add android, ios, mac?
    (False, True, "Composite Document File V2 Document", "ms-excel", "xls",
     "Excel Spreadsheet", (WINDOWS,)), # @todo, add android, ios, mac?
    (False, False, "RIFF", "x-wav", "wav", "WAVE Audio File", (WINDOWS,)),
    (False, False, "icon", "image/x-icon", "ico", "Icon File", (WINDOWS,)),
    (False, False, "Apple HFS", "octet-stream", "ico", "Icon File",
     (MACOS,)),
    (False, False, "ISO Media", "video/mp4", "mp4", "MPEG-4 Video File",
     (WINDOWS, MACOS)),
    (False, False, "Debian binary package", "vnd.debian.binary-package", "deb",
     "Debian Software Package", (LINUX,)),
    (False, False, "RealMedia file", "vnd.rn-realmedia", "rm",
     "RealMedia File", (WINDOWS, LINUX, MACOS)),
    (False, False, "COM executable", "application", "com", "DOS Command File",
     (WINDOWS,)),
    (False, False, "PNG", "png", "png", "Portable Network Graphic",
     (WINDOWS,)),
    (False, True, "Python script,", "x-python", "py", "Python Script",
     (WINDOWS, MACOS, LINUX)),
    (False, False, "zlib", "zlib", "dmg", "Apple Disk Image", (MACOS,)),
    (False, True, "Composite Document File V2", "msword", "doc",
     "Microsoft Word Document", (WINDOWS,)), # todo
    (False, True, "PDF", "pdf", "pdf", "Portable Document Format File",
     (WINDOWS,)), # todo
    (False, True, "Macromedia Flash data", "x-shockwave-flash", "swf",
     "Shockwave Flash Movie", (WINDOWS,)), # todo
    (False, True, "Composite Document File V2 Document", "ms-powerpoint",
     "ppt", "PowerPoint Presentation", (WINDOWS,)), # todo
    (False, False, "Microsoft Cabinet archive data", "vnd.ms-cab", "cab",
     "Windows Cabinet File", (WINDOWS,)),
    (False, True, "Composite Document File V2 Document", "msi", "msi",
     "Windows Installer Package", (WINDOWS,)),
    (False, True, "contains:MPEG", "mpeg", "mp3", "MP3 Audio File", (WINDOWS,)), # todo
    (False, True, "RIFF", "msvideo", "avi", "Audio Video Interleave File",
     (WINDOWS,)),
    (False, False, "JPEG", "jpeg", "jpg", "JPEG Image", (WINDOWS,)), # todo
    (False, True, "Rich Text", "rtf", "rtf", "Rich Text Format File",
     (WINDOWS,)),
    (False, True, "Macromedia Flash Video", "x-flv", "flv", "Flash Video File",
     (WINDOWS,)), #todo
    (False, True, "Microsoft PowerPoint",
     "openxmlformats-officedocument.presentationml.presentation", "pptx",
     "PowerPoint Open XML Presentation", (WINDOWS,)), #todo
    (False, False, "PostScript document", "postscript", "ps",
     "Encapsulated PostScript File", (WINDOWS,)), #todo

    (False, True, "PC bitmap", "x-ms-bmp", "bmp", "Bitmap Image File",
     (WINDOWS,)),
    (False, True, "POSIX tar", "tar", "tar", "Consolidated Unix File Archive",
     (LINUX,)),
    (False, False, "GIF image data", "gif", "gif",
     "Graphical Interchange Format File", (WINDOWS,)), #todo
    (False, False, "MS Windows shortcut", "octet-stream", "lnk",
     "Windows Shortcut", (WINDOWS,)),
    (False, True, "OpenDocument Text", "oasis.opendocument.text", "odt",
     "OpenDocument Text Document", (WINDOWS,)), #todo
    (False, True, "OpenOffice", "octet-stream", "odt",
     "OpenDocument Text Document", (WINDOWS,)), #todo
    (False, False, "Adobe Photoshop Image", "adobe.photoshop", "psd",
     "Adobe Photoshop Document", (WINDOWS, MACOS)),
    (False, False, "Microsoft ASF", "ms-asf", "asf",
     "Advanced Systems Format File", (WINDOWS,)),
    (False, False, "3GPP", "octet-stream", "3gp", "3GPP Multimedia File",
     (WINDOWS,)), #todo
    (False, False, "Google Chrome extension", "x-chrome-extension", "crx",
     "Chrome Extension", (WINDOWS, LINUX, MACOS)),
    (False, False, "compiled Java class", "java-applet", "class",
     "Java Class File", (WINDOWS, MACOS)),
    (False, True, "RAR", "rar", "rar", "WinRAR Compressed Archive",
     (WINDOWS,)),
    (False, True, "Hangul (Korean) Word Processor", "hwp", "hwp",
     "Hangul (Korean) Word Processor", (WINDOWS,)), #todo
    (False, True, "Microsoft Word",
     "openxmlformats-officedocument.wordprocessingml.document", "docx",
     "Microsoft Word Open XML Document", (WINDOWS,)), #todo
    (False, False, "PHP", "x-php", "php", "PHP Source Code File", (WINDOWS,)), #todo
    (False, False, "Intel serial flash", "octet", "rom", "N64 Game ROM File",
     (WINDOWS,)), # todo
    (False, True, "Microsoft Excel",
     "openxmlformats-officedocument.spreadsheetml.sheet", "xlsx",
     "Microsoft Excel Open XML Spreadsheet", (WINDOWS,)), #todo
    (True, False, "Composite Document File V2 Document, Can't read SAT",
     "application/CDFV2", SAT),
    (True, False, "Composite Document File V2 Document, Cannot read section",
     "application/CDFV2", SECTION),
    # @todo should this be .torrent?
    (False, False, "BitTorrent", "x-bittorrent", "bittorrent",
     "Bittorent link",(WINDOWS, MACOS)),
    # todo
    (False, False, "SVG", "svg+xml", "svg", "Scalable vector graphics",
     (WINDOWS,)),  # todo
    (False, True, "OpenDocument Spreadsheet", "opendocument.spreadsheet",
     "ods", "OpenDocument Spreadsheet", (WINDOWS,)),  # todo
    (False, True, "OpenDocument", "opendocument.presentation", "odp",
     "OpenDocument Presentation", (WINDOWS,)),  # todo
    (False, True, "compiled Java class", "x-java-applet", "class",
     "Java class file", (WINDOWS,)),  # todo
    # (False, False, "data","octet-stream","ace","-",("widows")),
    (False, True, "PE32", "x-dosexec", "exe", "Portable executable",
     (WINDOWS,)),
    # (False, False, "data","octet-stream","mscompress","-",("windows")),
    # @todo what should this be?
    (False, False, "MS Compress", "octet-stream", "mscompress",
     "Microsoft (de)compressor", (WINDOWS,)),
    (False, False, "Bourne-Again shell", "x-shellscript", "sh", "Shell script",
     (LINUX,)),
    (False, False, "GIMP XCF image", "x-xcf", "xcf", "GIMP XFC file",
     (WINDOWS, LINUX, MACOS)),
    (False, False, "MIDI", "midi", "midi",
     "Musical Instrument Digital Interface", (WINDOWS,)),
    (False, False, "MS-DOS", "x-dosexec", "exe", "DOS MZ executable ",
     (WINDOWS,)),
    (False, False, "Macromedia Flash", "x-shockwave-flash", "flv",
     "Flash Video file", (WINDOWS,)),
    # todo
    (False, False, "Perl script", "x-perl", "perl", "Perl script",
     (WINDOWS, LINUX)),
    # todo
    # (False, False, "None","None","gul","-",("windows")),
    (False, False, "Targa", "x-tga", "tga",
     "Truevision Graphics Adapter image file", (WINDOWS, MACOS)),  # todo
    (False, False, "Ogg", "ogg", "ogg", "Free open container format ",
     (WINDOWS, MACOS)),
    (False, False, "KGB", "octet-stream", "kgb", "Discontinued file archiver ",
     (WINDOWS, LINUX)),
    (False, False, "ISO 9660", "x-iso9660-image", "iso", "ISO Image",
     (WINDOWS,)),
    # (False, False, "data","octet-stream","machfs","-",("windows")),
    # (False, False, "data","octet-stream","asd","-",("windows")),
    (False, False, "Symbian", "x-sisx-app", "sis",
     "Software Installation Script", (WINDOWS,)),
    (False, False, "iOS App", "x-ios-app", "ipa",
     "iOS application archive file", (IOS,)),
    (False, False, "AppleSingle", "octet-stream", "applesingle",
     "Mac File format", (MACOS,)),
    (False, False, "TeX font", "x-tex-tfm", "latex", "LaTeX file format",
     (WINDOWS, LINUX)),  # todo
    (False, False, "bzip2", "x-bzip2", "bzip", "Compressed file", (LINUX,)),
    (False, False, "AppleDouble", "octet-stream", "appledouble",
     "iOS application archive file", (MACOS,)),
    # http://fileformats.archiveteam.org/wiki/Mach-O
    (False, False, "Mach-O", "x-mach-binary", "macho",
     "File for executables, object code, shared libraries, dynamically-loaded"
     " code, and core dumps",
     (MACOS,)),
    (False, False, "ISO", "quicktime", "qt", "QuickTime file", (MACOS,)),
    #(False, False, "text", "plain", "palmos", "OS for pda's or smarthpones",
    # (WINDOWS)),  # todo
    # (False, False, "data","octet-stream","blackhole","-",("windows")),
    # (False, False, "text","plain","c","C/C++ Source Code File",("windows")),
    # (False, False, "None","None","jpeg","-",("windows")),
    (False, False, "awk", "x-awk", "awk", "Script for text processing",
     (LINUX,)),
    # (False, False, "data","octet-stream","emf","-",("windows")),
    (False, False, "ARJ", "x-arj", "arj", "Compressed file archive",
     (WINDOWS, MACOS)),
    # (False, False, "data","octet-stream","dyalog","-",("windows")),
    # (False, False, "data","octet-stream","coff","-",("windows")),
    (False, False, "Apple binary property", "octet-stream", "apple",
     "Apple binary", (MACOS,)),
    (False, False, "Adobe InDesign", "octet-stream", "indd",
     "InDesign project file", (WINDOWS,)),  # todo
    #(False, False, "text", "plain", "ruby", "Ruby interpreted file",
    # (WINDOWS, MACOS, LINUX)),
    (False, False, "MPEG", "mpeg", "mpeg", "Compression for video and audio",
     (WINDOWS,)),
    # (False, False, "None","None","fla","Adobe Animate Animation",("windows")), #todo
    (False, False, "E-book", "octet-stream", "ebook", "Ebook file",
     (WINDOWS,)),
    (False, False, "gzip", "gzip", "gz", "Compression file", (WINDOWS,)),
    # todo
    #(False, False, "text", "plain", "cookie", "Internet Explorer cookie",
    # (WINDOWS)),
    (False, False, "ELF", "application", "elf", "Linux Executable", (LINUX,)),
    (False, False, "Apple binary property", "octet-stream", "appleplist",
     "Apple binary", (MACOS,)),
    (False, False, "MS-DOS", "x-dosexec", "exe", "Executable", (WINDOWS,)),
    (False, False, "PE32", "x-dosexec", "dll", "Dynamic linked library",
     (WINDOWS,)),
    (False, False, "FLAC", "x-flac", "flac", "Free lossless audio codec",
     (WINDOWS)),
    # todo
    (False, False, "SMTP", "rfc822", "email", "Email file", (WINDOWS,)),
    (False, False, "FLC", "x-flc", "flc", "Animation file", (MACOS,)),
    # (False, False, "text","plain","text","-",("windows")),
    # (False, False, "data","octet-stream","ttf","TrueType Font",("windows")),
    (False, False, "ARC", "x-arc", "arc", "Compressed file",
     (WINDOWS, MACOS)),
    # https://fileinfo.com/extension/dzip
    (False, False, "Dzip", "octet-stream", "dzip", "Witcher 2 game file",
     (WINDOWS,)),
    (False, False, "7-zip", "x-7z-compressed", "7zip", "Compressed archive",
     (WINDOWS,)),
    # (False, False, "text","plain","pascal","-",("windows")),
    (False, False, "JNG", "x-jng", "jng", "Image file related to PNG",
     (WINDOWS,)),
    (False, False, "capture", "tcpdump.pcap", "cap", "Network traffic data",
     (WINDOWS,)),
    (False, False, "Mach-O", "x-mach-binary", "mac", "Bitmap graphic",
     (MACOS,)),
    (False, True, "Microsoft", "octet", "doc", "Microsoft Document", (WINDOWS,)),
    (True, True, "Zip", "zip", ZIP),
    (True, True, "(JAR)", "java-archive", JAR),
    (True, False, "data", "octet", OCTET),
    (True, False, "XML", "xml", XML),
    (False, True, "HTML document,", "html", "html", "Hypertext Markup Language File",
     (WINDOWS,)),  # todo
    (True, False, "text", "text", Text),
    (True, False, "text", "plain", Text),

]

def identify(f):
    # return: selected, name, extension, platform
    # Loop through every potential match
    for match in matches:
        function, selected, magic, mime = match[:4]
        # Check if it matches
        tokens = all(elem in f.magic.split(" ") for elem in magic.split(" "))
        if tokens and mime in f.mime:
            # If the match is a function
            # Check if there is already a match found (on a non function match)
            # The non function matches are narrower
            if function:
                return (selected, *match[4](f))
            else:
                # @todo, decide what to do when multiple matches
                # For now, return
                return selected, match[5], match[4], match[6]
