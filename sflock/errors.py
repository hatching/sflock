# Copyright (C) 2020 - 2021 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

class Errors:
    NO_ERROR = None
    NOT_SUPPORTED = "failed_not_supported"
    MISSING_DEPENDENCY = "failed_missing_dependency"
    DECRYPTION_FAILED = "failed_decryption_failed"
    INVALID_ARCHIVE = "failed_invalid_archive"
    UNPACK_FAILED = "failed_unpacking"
    NOTHING_EXTRACTED = "failed_nothing_extracted"
    CANCELLED_SYMLINK = "cancelled_malicious_symlink"
    TOTAL_TOO_LARGE = "cancelled_total_size_too_large"
    CANCELLED_DIR_TRAVERSAL = "cancelled_directory_traversal"
    ZIPJAIL_FAIL = "failed_zipjail_error"
