import re
from sflock.ident import javascript, powershell, wsf, visualbasic, java, ruby

ttf_hdr = (
    b'\x00\x01\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00'
)

WINDOWS = "windows"
MACOS = "darwin"
LINUX = "linux"
ANDROID = "android"
IOS = "ios"
ANY_DESKTOP = (WINDOWS, MACOS, LINUX)
ANY = (WINDOWS, MACOS, LINUX, ANDROID, IOS)

def HTML(f):
    if wsf(f):
        return "Windows script file", "wsf", (WINDOWS,)
    return "Hypertext Markup Language File", "html", ANY

def XML(f):
    if b"application/vnd.openxmlformats-officedocument.presentationml" in f.contents:
        return "Office file", "xml", (WINDOWS,)
    if b"application/vnd.openxmlformats-officedocument" in f.contents:
        return "Office file", "doc", (WINDOWS,)
    if wsf(f):
        return "Windows script file", "wsf", (WINDOWS,)
    return "XML file", "xml", ANY

def SAT(f):
    if f.get_child("ppt/presentation.xml"):
        return "Powerpoint", "ppt", (WINDOWS,)
    return None, None, None

def SECTION(f):
    return 'CDF file', 'cdf', (WINDOWS,)

def Text(f):
    if javascript(f):
        return "Javascript file", "js", (WINDOWS,)
    if powershell(f):
        return "Powershell script", "ps1", (WINDOWS,)
    if wsf(f):
        return "Windows script file", "wsf", (WINDOWS,)
    if visualbasic(f):
        return "Visual basic file", "vb", (WINDOWS,)
    if ruby(f):
        return "Ruby file", "rb", (WINDOWS,)
    if f.contents.startswith(b"WEB"):
        return "IQY file", "iqy", (WINDOWS,)
    if f.contents.startswith(b"ID;"):
        return "SYLK file", "slk", (WINDOWS,)
    if b"Content-Type: text/html;" in f.contents:
        return "Mht file", "mht", (WINDOWS,)
   
    return "Text", "txt", ANY

def ZIP(f):
    for i in f.children:
        if i.filename.lower() == "workbook.xml":
            return "Excel document", "xlsx", (WINDOWS,)
        if i.filename.lower() == "worddocument.xml":
            return "Word document", "docx", (WINDOWS,)
    if java(f):
        return "JAR file", "jar", (WINDOWS,)
    return "ZIP file", "zip", (WINDOWS,)

def JAR(f):
    if f.get_child("AndroidManifest.xml"):
        return "Android Package File", "apk", (ANDROID,)

    return "Java Archive File", "jar", (WINDOWS,)

def OCTET(f):
    if wsf(f):
        return "Windows script file", "wsf", (WINDOWS,)
    if f.contents.startswith(ttf_hdr):
        return "TrueType Font", "ttf", (WINDOWS,)
    return "octet", "", (WINDOWS,)

# This function is used to distinct DLL and EXE. This was unable to work on
# magic and mime. Because DLL files are matching positive on EXE mime/magic
def PE32(f):
    if "DLL" in f.magic:
        return "DLL file", "dll", (WINDOWS,)
    return "Exe file", "exe", (WINDOWS,)

def FLASH(f):
    if "(compressed)" in f.magic:
        return "SWF file", "swf", (WINDOWS,)
    return "FLV file", "flv", (WINDOWS,)

def EXCEL(f):
    content = f.get_child("[Content_Types].xml")
    if b"ContentType=\"application/vnd.ms-excel.sheet.macroEnabled" in content.contents:
        return "Microsoft Excel Open XML Spreadsheet", "xlsm", (WINDOWS,)
    if b"ContentType=\"application/vnd.ms-excel.sheet.binary.macroEnabled.main" in content.contents:
        return "Microsoft Excel Open XML Spreadsheet", "xlsb", (WINDOWS,)
    return "Microsoft Excel Open XML Spreadsheet", "xlsx", (WINDOWS,)

def POWERPOINT(f):
    content = f.get_child("[Content_Types].xml")
    if b"ContentType=\"application/vnd.ms-powerpoint.slideshow.macroEnabled" in content.contents:
        return "PowerPoint Open XML Presentation", "ppsm", (WINDOWS,)
    if b"ContentType=\"application/vnd.openxmlformats-officedocument.presentationml.slideshow" in content.contents:
        return "PowerPoint Open XML Presentation", "ppsx", (WINDOWS,)
    if b"ContentType=\"application/vnd.ms-powerpoint.presentation.macroEnabled" in content.contents:
        return "PowerPoint Open XML Presentation", "pptm", (WINDOWS,) 
    return "PowerPoint Open XML Presentation", "pptx", (WINDOWS,)

def MICROSOFT(f):
    if f.get_child("[Content_Types].xml"):
        return "Excel theme", "thmx", (WINDOWS,)
    return "Microsoft Document", "doc", (WINDOWS,)

# The magic and mime of a file will be used to match it to an extension or
# a function.
#   An extension will be used if the magic and mime are enough to distinct
#       different file types.
#   A function will be used to distinct file types on content.
#
# The default matches are designed to be order independent.
# This means the matches are made very specific for an extension.
# At first the string matches are used for identification,
# if the file does not match, the function matches are used.
string_matches = [
    # A string match tuple contains 7 elements.
    #   boolean: set True if string match
    #   boolean: set True if extension should be analysed
    #   list[] of strings:
    #       This list will be matched against the file magic
    #         The magic of the file is tokenized by splitting it on spaces.
    #         ex.: "PE32 (DLL) EXE" --> ["PE32", "(DLL)", "EXE"]
    #   string: Checks if mime contains this string.
    #   string: The extension for the match.
    #   string: A human friendly name of the match.
    #   string tuple: The platforms that support the extension.

    #
    # Office related
    #
    (True, ['Composite', 'Document', 'File', 'V2', 'Document'],
     "ms-excel", "xls",
     "Excel Spreadsheet", (WINDOWS,)),
    (True, ['Composite', 'Document', 'File', 'V2', 'Document'],
     "ms-powerpoint", "ppt", "PowerPoint Presentation", (WINDOWS,)),
    (True, ['Composite', 'Document', 'File', 'V2'], "msword", "doc",
     "Microsoft Word Document", (WINDOWS,)),  
    (True, ['OpenDocument', 'Text'], "oasis.opendocument.text", "odt",
     "OpenDocument Text Document", ANY),
    (True, ['OpenOffice'], "octet-stream", "odt",
     "OpenDocument Text Document", (WINDOWS,)),
    (True, ['Hangul', '(Korean)', 'Word', 'Processor'], "hwp", "hwp",
     "Hangul (Korean) Word Processor", (WINDOWS,)),
    (True, ['Microsoft', 'Word'],
     "openxmlformats-officedocument.wordprocessingml.document", "docx",
     "Microsoft Word Open XML Document", (WINDOWS,)),
    (True, ['OpenDocument', 'Spreadsheet'], "opendocument.spreadsheet",
     "ods", "OpenDocument Spreadsheet", (WINDOWS,)),
    (True, ['OpenDocument'], "opendocument.presentation", "odp",
     "OpenDocument Presentation", (WINDOWS,)),
    (True, ['CDFV2', 'Microsoft', 'Excel'], "ms-excel", "xlsx",
     "Excel Spreadsheet", (WINDOWS,)),
    (True, ['Composite', 'Document', 'File', 'V2', 'Document'],
     "ms-office", "cdf", "CDF file", (WINDOWS,)), # TODO, look at these cdf files and the right extension
    (False, ['CDFV2', 'Encrypted'], 'encrypted', "cdf", "CDF file",
     (WINDOWS,)), # TODO, look at these cdf files and the right extension
    (False, ['CDFV2', 'Microsoft', 'Outlook'],
     'ms-outlook', "cdf", "CDF file", (WINDOWS,)),  # TODO, look at these cdf files and the right extension

    #
    # Archive/compression related
    #
    (False, ['7-zip'], "x-7z-compressed", "7zip", "Compressed archive",
     (WINDOWS,)),
    (False, ['bzip2'], "x-bzip2", "bzip", "Compressed file", (LINUX,)),
    (False, ['gzip'], "gzip", "gz", "Compression file", (WINDOWS,)),
    (True, ['ACE', 'archive'], "octet-stream", "ace", "ACE archive",
     (WINDOWS,)),
    (False, ['MS', 'Compress'], "octet-stream", "zip",
     "Microsoft (de)compressor", (WINDOWS,)),
    (False, ['Microsoft', 'Cabinet', 'archive', 'data'], "vnd.ms-cab",
     "cab", "Windows Cabinet File", (WINDOWS,)),
    (True, ['POSIX', 'tar'], "tar", "tar",
     "Consolidated Unix File Archive", (LINUX,)),
    (True, ['RAR'], "rar", "rar", "WinRAR Compressed Archive",
     (WINDOWS,)),
    (False, ['KGB'], "octet-stream", "kgb",
     "Discontinued file archiver ",
     (WINDOWS, LINUX)),
    (False, ['ASD', 'archive'], "octet-stream", "asd",
     "ASD archive", (WINDOWS,)),
    (False, ['ARJ'], "x-arj", "arj", "Compressed file archive",
     (WINDOWS, MACOS)),
    (False, ['ARC'], "x-arc", "arc", "Compressed file",
     (WINDOWS, MACOS)),
    
    #
    # Apple related
    #
    (False, ['Apple', 'HFS'], "octet-stream", "ico", "Icon File",
     (MACOS,)),
    (False, ['zlib'], "zlib", "dmg", "Apple Disk Image", (MACOS,)),
    (False, ['AppleSingle'], "octet-stream", "as",
     "Mac File format", (MACOS,)),
    (False, ['AppleDouble'], "octet-stream", "adf",
     "iOS application archive file", (MACOS,)),
    (False, ['Apple', 'binary', 'property'], "octet-stream",
     "plist", "Apple binary", (MACOS,)),
    (False, ['iOS', 'App'], "x-ios-app", "ipa",
     "iOS application archive file", (IOS,)),
    (False, ['Macintosh', 'HFS'], "octet-stream", "hfs",
     "Macintosh HFS", (MACOS,)),
    (False, ['Symbian'], "x-sisx-app", "sisx",
     "Software Installation Script", (MACOS,)),
    (False, ['Mach-O'], "x-mach-binary", "o", "Bitmap graphic",
     (MACOS,)),

    #
    # Visual images
    #
    (False, ['PNG'], "png", "png", "Portable Network Graphic",
     (WINDOWS,)),
    (False, ['JPEG'], "jpeg", "jpg", "JPEG Image", (WINDOWS,)), 
    (False, ['SVG'], "svg+xml", "svg", "Scalable vector graphics",
     (WINDOWS,)),  
    (True, ['PC', 'bitmap'], "x-ms-bmp", "bmp", "Bitmap Image File",
     (WINDOWS,)),
    (False, ['Targa'], "x-tga", "tga",
     "Truevision Graphics Adapter image file", (WINDOWS, MACOS)), 
    (False, ['GIF', 'image', 'data'], "gif", "gif",
     "Graphical Interchange Format File", (WINDOWS,)),
    (False, ['JNG'], "x-jng", "jng", "Image file related to PNG",
     (WINDOWS,)),
    (False, ['GIMP', 'XCF', 'image'], "x-xcf", "xcf", "GIMP XFC file",
     (WINDOWS, LINUX, MACOS)),
    (False, ['TIFF'], "tiff", "tiff", "Tagged Image File Format",
     (WINDOWS, LINUX)),  # @todo, add android, ios, mac?
    (False, ['icon'], "image/x-icon", "ico", "Icon File", (WINDOWS,)),

    #
    # Audio / video 
    #
    (False, ['RIFF'], "x-wav", "wav", "WAVE Audio File", (WINDOWS,)),
    (True, ['Macromedia', 'Flash', 'data', '(compressed)'],
     "x-shockwave-flash", "swf", "Shockwave Flash Movie", (WINDOWS,)),  # todo
    (True, ['RIFF'], "msvideo", "avi", "Audio Video Interleave File",
     (WINDOWS,)),
    (True, ['Macromedia', 'Flash', 'Video'], "x-flv", "flv",
     "Flash Video File", (WINDOWS,)),  
    (False, ['ISO'], "quicktime", "qt", "QuickTime file", (MACOS,)), # todo, make magic more specific
    (False, ['MPEG', 'sequence'], "", "mpeg",
     "Compression for video and audio",
     (WINDOWS,)),
    (False, ['MPEG', 'transport'], "", "mpeg",
     "Compression for video and audio",
     (WINDOWS,)),
    (False, ['PCH', 'ROM'], "octet", "rom", "N64 Game ROM File",
     (WINDOWS,)),
    (False, ['ISO', 'Media'], "video/mp4", "mp4", "MPEG-4 Video File",
     (WINDOWS, MACOS)),
    (True, ['contains:MPEG'], "mpeg", "mp3", "MP3 Audio File",
     (WINDOWS,)),  
    (False, ['3GPP', 'MPEG', 'v4'], "octet-stream", "3gp",
     "3GPP Multimedia File", (WINDOWS,)), 
    (False, ['FLAC'], "x-flac", "flac", "Free lossless audio codec",
     (WINDOWS)),    
    (False, ['FLC'], "x-flc", "flc", "Animation file", (MACOS,)),
    (False, ['RealMedia', 'file'], "vnd.rn-realmedia", "rm", "RealMedia file", (WINDOWS,)), 
    
    #
    #  Scripts
    #
    (True, ['Python', 'script'], "x-python", "py", "Python Script",
     (WINDOWS, MACOS, LINUX)),    
    (False, ['PostScript', 'document'], "postscript", "ps",
     "Encapsulated PostScript File", (WINDOWS,)),  
    (False, ['PHP'], "x-php", "php", "PHP Source Code File",
     (WINDOWS,)),
    (False, ['Perl', 'script'], "x-perl", "perl", "Perl script",
     (WINDOWS, LINUX)),
    (False, ['Bourne-Again', 'shell'], "x-shellscript", "sh",
     "Shell script", (LINUX,)),
    (False, ['Ruby', 'script'], "x-ruby", "rb",
     "Ruby interpreted file", (WINDOWS,)),

    #
    # Binaries
    #
    (False, ['COM', 'executable'], "application", "com",
     "DOS Command File", (WINDOWS,)),    
    (False, ['Debian', 'binary', 'package'],
     "vnd.debian.binary-package", "deb", "Debian Software Package", (LINUX,)),
    (True, ['(DLL)'], "x-dosexec", "dll", "Dynamic linked library",
     (WINDOWS,)), 
    (False, ['MS-DOS'], "x-dosexec", "exe", "Executable", (WINDOWS,)),
    (False, ['ELF'], "application", "elf", "Linux Executable",
     (LINUX,)),
    (False, ['MS-DOS'], "x-dosexec", "exe", "DOS MZ executable ",
     (WINDOWS,)), 
    (True, ['Composite', 'Document', 'File', 'V2', 'Document'], "msi",
     "msi", "Windows Installer Package", (WINDOWS,)),

    (False, ['Dzip'], "octet-stream", "dzip", "Witcher 2 game file",
     (WINDOWS,)),
    (False, ['RPM'], "rpm", "rpm", "Red Hat Package Manager File", (LINUX,)),   
    (True, ['PDF'], "pdf", "pdf", "Portable Document Format File",
     (WINDOWS,)),  
    (True, ['Rich', 'Text'], "rtf", "rtf", "Rich Text Format File",
     (WINDOWS,)),
    (False, ['MS', 'Windows', 'shortcut'], "octet-stream", "lnk",
     "Windows Shortcut", (WINDOWS,)),
    (False, ['Adobe', 'Photoshop', 'Image'], "adobe.photoshop", "psd",
     "Adobe Photoshop Document", (WINDOWS, MACOS)),
    (False, ['Microsoft', 'ASF'], "ms-asf", "asf",
     "Advanced Systems Format File", (WINDOWS,)),
    (False, ['Google', 'Chrome', 'extension'], "x-chrome-extension",
     "crx", "Chrome Extension", (WINDOWS, LINUX, MACOS)),
    (False, ['compiled', 'Java', 'class'], "java-applet", "class",
     "Java Class File", (WINDOWS, MACOS)),
    (False, ['Intel', 'serial', 'flash'], "octet", "rom",
     "N64 Game ROM File",
     (WINDOWS,)),  # todo
    (False, ['BitTorrent'], "x-bittorrent", "bittorrent",
     "Bittorent link", (WINDOWS, MACOS)),
    (True, ['compiled', 'Java', 'class'], "x-java-applet", "class",
     "Java class file", (WINDOWS,)),  # todo
    (False, ['MIDI'], "midi", "midi",
     "Musical Instrument Digital Interface", (WINDOWS,)),
    (False, ['Ogg'], "ogg", "ogg", "Free open container format ",
     (WINDOWS, MACOS)),
    (False, ['ISO', '9660'], "x-iso9660-image", "iso", "ISO Image",
     (WINDOWS,)),
    (False, ['TeX', 'font'], "x-tex-tfm", "latex", "LaTeX file format",
     (WINDOWS, LINUX)),  # todo
    (False, ['awk'], "x-awk", "awk", "Script for text processing",
     (LINUX,)),
    (False, ['Adobe', 'InDesign'], "octet-stream", "indd",
     "InDesign project file", (WINDOWS,)),  # todo
    (False, ['Windows', 'Enhanced', 'Metafile'], "octet-stream", "emf",
     "Windows enhanced metafile", (WINDOWS,)),
    (False, ['E-book'], "octet-stream", "ebook", "Ebook file",
     (WINDOWS,)),
    (False, ['SMTP'], "rfc822", "email", "Email file", (WINDOWS,)),
    (False, ['TrueType', 'Font'], "font-sfnt", "ttf", "TrueType Font",
     (WINDOWS)),
    (False, ['capture'], "tcpdump.pcap", "pcap", "Network traffic data",
     (WINDOWS,)),
    (False, ['capture'], "octet-stream", "pcap", "Network traffic data",
     (WINDOWS,)),
    (
    False, ['Netscape', 'cookie'], "plain", "iecookie", "Cookie for ie",
    (WINDOWS)),
]

# Add function variables
func_matches = [
    (False,
     ['Composite', 'Document', 'File', 'V2', 'Document', "Can't", 'read',
      'SAT'], "application/CDFV2", SAT),
    (False,
     ['Composite', 'Document', 'File', 'V2', 'Document', 'Cannot', 'read',
      'section'],
     "application/CDFV2", SECTION),
    (True, ['Zip'], "zip", ZIP),
    (True, ['(JAR)'], "java-archive", JAR),
    (False, ['data'], "octet", OCTET),
    (False, ['XML'], "xml", XML),
    (True, ['HTML', 'document'], "html", HTML),
    (False, ['text'], "text", Text),
    (False, ['text'], "plain", Text),
    (True, ['PE32'], "x-dosexec", PE32),
    (False, ['Macromedia', 'Flash', 'data'], "x-shockwave-flash", FLASH),
    (True, ['Microsoft', 'Excel'],
     "openxmlformats-officedocument.spreadsheetml.sheet", EXCEL),
    (True, ['Microsoft', 'PowerPoint'],
     "openxmlformats-officedocument.presentationml.presentation", POWERPOINT),
    (True, ['Microsoft'], "octet", MICROSOFT)
]

def identify(f):
    # return: selected, name, extension, platform
    # Loop through every potential match
    fmagic = [i.replace(",", "") for i in f.magic.split(" ")]

    for match in string_matches:
        selected, magic, mime = match[:3]
        # Check if it matches
        tokens = all(elem in fmagic for elem in magic)
        if tokens and mime in f.mime:
            # If the match is a function
            # Check if there is already a match found (on a non function match)
            # The non function matches are narrower
            return selected, match[4], match[3], match[5]
    
    for match in func_matches:
        selected, magic, mime = match[:3]
        # Check if it matches
        tokens = all(elem in fmagic for elem in magic)
        if tokens and mime in f.mime:
            # If the match is a function
            # Check if there is already a match found (on a non function match)
            # The non function matches are narrower
            return (selected, *match[3](f))
           