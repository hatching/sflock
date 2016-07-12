#!/usr/bin/env python
# Copyright (C) 2015 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from setuptools import setup

setup(
    name="SFlock",
    version="0.1",
    author="Jurriaan Bremer",
    author_email="jbr@cuckoo.sh",
    packages=[
        "sflock",
        "sflock.unpack",
        "sflock.test",
        "sflock.data",
        "sflock.data.test",
    ],
    scripts=[
        "bin/sflock",
    ],
    url="http://sflock.org/",
    license="GPLv3",
    description="Sample staging and detonation utility",
    include_package_data=True,
    package_data={
        "sflock.data": ["*.*"],
    },
    install_requires=[
        "python-magic==0.4.12",
    ],
)
