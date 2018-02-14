# sflock

[![Build Status](https://travis-ci.org/jbremer/sflock.svg?branch=master)](https://travis-ci.org/jbremer/sflock)
[![Windows Build Status](https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true)](https://ci.appveyor.com/project/jbremer/sflock)
[![Coverage Status](https://coveralls.io/repos/github/jbremer/sflock/badge.svg?branch=master)](https://coveralls.io/github/jbremer/sflock?branch=master)
[![codecov](https://codecov.io/gh/jbremer/sflock/branch/master/graph/badge.svg)](https://codecov.io/gh/jbremer/sflock)

Sample staging &amp; detonation utility to be used as unpacking engine for
other analysis tools.

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
$ sudo apt-get install p7zip-full rar unace-nonfree cabextract
```

Installation of sflock itself may be done as follows.

```bash
$ sudo pip install -U sflock
```

Or in a virtualenv environment.

```bash
(venv)$ pip install -U sflock
```

Installation (Windows)
======================

Since version 0.2 sflock properly supports Windows-based operating systems.
However, as-is only 32-bit Python setups are fully supported, as currently no
support exists for libmagic in 64-bit Python, see also
https://github.com/ahupp/python-magic#dependencies.

To simplify the setup phase, sflock ships the required 32-bit binaries to use
libmagic under Windows and as such Windows support works flawlessly.

Note: on Windows the `7z`, `ace`, `cab`, and `rar` file formats are not
supported.

Installation (Mac OS X)
=======================

Since version 0.2 sflock properly supports Mac OS X-based operating systems.
One does have to manually install `libmagic` though. This may be done through
the `brew` package manager.

```bash
$ brew update
$ brew install libmagic
```

Note: on Mac OS X the `7z`, `ace`, `cab`, and `rar` file formats are not
supported.

Supported archives
==================

SFlock supports a number of (semi-)archive types, sorted by extension:

* .7z (7-Zip archive, `requires native tooling`)
* .ace (ACE archive, `requires native tooling`)
* .bup (McAfee quarantine files)
* .cab (Microsoft Cabinet archive, `requires native tooling`)
* .eml (MIME RFC 822 email representation)
* .msg (Outlook mail message)
* .mso (Microsoft Office Macro reference file)
* .pdf (Attachments embedded in PDF files)
* .rar (RAR archive, `requires native tooling`)
* .tar (Unix file archive)
* .tar.bz2 (bzip2 compressed Unix file archive)
* .tar.gz (gzip compressed Unix file archive)
* .zip (ZIP archive)

Security
========

Due to its nature of unpacking malicious archives with, depending on the
extension, native tools (i.e., *.7z*, *.ace*, *.cab*, *.rar*), it is
important that such operations happen securely. SFlock therefore wraps
execution of the native tools in [zipjail][], a usermode sandbox written
exactly for this purpose.

[zipjail]: https://github.com/jbremer/tracy/tree/master/src/zipjail
