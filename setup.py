# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018-2019 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from setuptools import setup

setup(
    name="SFlock",
    version="0.3.9",
    author="Hatching B.V.",
    author_email="jbr@hatching.io",
    packages=[
        "sflock",
        "sflock.unpack",
        "sflock.data",
    ],
    entry_points={
        "console_scripts": [
            "sflock = sflock.main:main",
        ],
    },
    url="http://sflock.org/",
    license="GPLv3",
    description="Sample staging and detonation utility",
    include_package_data=True,
    install_requires=[
        "click==6.6",
        "cryptography>=2.1",
        "olefile==0.43",
        "peepdf>=0.4.1",
        "python-magic==0.4.12",
    ],
)
