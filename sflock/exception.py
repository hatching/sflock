# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.


class SflockException(Exception):
    pass


class IncorrectUsageException(SflockException):
    pass


class UnpackException(SflockException):
    pass


class DecoderException(SflockException):
    pass
