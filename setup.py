# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018-2019 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from setuptools import setup, find_packages
from distutils.util import convert_path

ver_module_ns = {}
ver_module = convert_path('sflock/__version__.py')
with open(ver_module) as fh:
    exec(fh.read(), ver_module_ns)
assert '__version__' in ver_module_ns
version = ver_module_ns['__version__']

setup(
    name="SFlock",
    version=version,
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
        "click",
        "cryptography>=2.1",
        "olefile>=0.43",
        # "peepdf>=0.4.1",
        "python-magic>=0.4.13",
    ],
)
