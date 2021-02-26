# Copyright (C) 2015-2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

class SflockException(Exception):
    pass

class IncorrectUsageException(SflockException):
    pass

class UnpackException(SflockException):

    def __init__(self, message, state=None):
        self.state = state
        super().__init__(message)

class NotSupportedError(UnpackException):
    pass

class DecryptionFailedError(UnpackException):
    pass

class IncorrectPasswordException(DecryptionFailedError):
    pass

class DecoderException(SflockException):
    pass

class MaxNestedError(SflockException):
    pass
