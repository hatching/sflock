# sflock

![example workflow](https://github.com/doomedraven/sflock/actions/workflows/pythonpackage.yml/badge.svg)

Sample staging &amp; detonation utility to be used as unpacking engine for
other analysis tools. Since version 0.3.14 sflock is compatible with Python >= 3.6

Birds tend to move around in flocks, therefore the sflock utility can digest a
flock of samples, but also inverse flocks, i.e., sflock unpacks various
archive file formats to extract embedded samples.

Simply put, sflock provides a staging area where binary data is investigated
and split into one or more files to be analyzed further by other tools. In
particular sflock focuses on integration and usage with Cuckoo Sandbox.

Installation
============

As-is sflock has been designed to be used to its full extent on
Ubuntu/Debian-like systems. For optimal usage it is recommended to install the
following packages alongside sflock. It is currently not possible to run the
unpackers that require native tooling support on non-Linux platforms.

```bash
$ sudo apt-get install p7zip-full rar unace-nonfree cabextract lzip libjpeg8-dev zlib1g-dev
```

Installation of sflock itself may be done as follows.

```bash
$ sudo pip install -U sflock2
```

Or in a virtualenv environment.

```bash
(venv)$ pip install -U sflock2
```

Supported archives
==================

SFlock supports a number of (semi-)archive types, sorted by extension:

* .7z (7-Zip archive, `requires native tooling`)
* .ace (ACE archive, `requires native tooling`)
* .bup (McAfee quarantine files)
* .cab (Microsoft Cabinet archive, `requires native tooling`)
* .daa (PowerISO, `requires included Linux native tooling`)
* .eml (MIME RFC 822 email representation)
* .gzip (gzip compressed data, `requires native tooling`)
* .iso (ISO file container, `requires native tooling`)
* .lzh (LZH/LHA archive, `requires native tooling`)
* .lz (Lzip compressed data, `requires native tooling`)
* .msg (Outlook mail message)
* .mso (Microsoft Office Macro reference file)
* .pdf (Attachments embedded in PDF files)
* .rar (RAR archive, `requires native tooling`)
* .tar (Unix file archive)
* .tar.bz2 (bzip2 compressed Unix file archive)
* .tar.gz (gzip compressed Unix file archive)
* .zip (ZIP archive)
* .win (Windows imaging (WIM) image)

Security
========

Due to its nature of unpacking malicious archives with, depending on the
extension, native tools (i.e., *.7z*, *.ace*, *.cab*, *.daa*, *.gzip*, *.iso*,
*.lzh*, and *.rar*), it is important that such operations happen securely.
SFlock therefore wraps execution of the native tools in [zipjail][], a
usermode sandbox written exactly for this purpose.

[zipjail]: https://github.com/jbremer/tracy/tree/master/src/zipjail
