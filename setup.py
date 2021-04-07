#!/usr/bin/env python
#
# Original work: Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Modified work: Copyright 2021 Averbis GmbH
# Distributed under the terms of the 3-clause BSD License.

import os

from setuptools import find_packages, setup

with open('src/sos_ruta/_version.py') as version:
    for line in version:
        if line.startswith('__version__'):
            __version__ = eval(line.split('=')[1])
            break

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    with open(os.path.join(CURRENT_DIR, "README.md"), "r") as ld_file:
        return ld_file.read()


setup(
    name="sos-ruta",
    version=__version__,
    description='SoS Notebook extension for the language Apache UIMA Ruta',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author='Averbis',
    license='3-clause BSD',
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    tests_require=[
        'testpath',
        'requests',
        'pytest',
        'nose',
        'selenium'
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'sos>=0.19.8', 'sos-notebook>=0.19.4', 'dkpro-cassis>=0.5.1'
    ],
    entry_points='''
                [sos_languages]
                ruta = sos_ruta.kernel:sos_Ruta
                '''
)
