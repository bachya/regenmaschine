"""
File: setup.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs

from setuptools import setup

try:
    # Python 3
    from os import dirname  # pylint: disable=ungrouped-imports
except ImportError:
    # Python 2
    from os.path import dirname

HERE = os.path.abspath(dirname(__file__))

with codecs.open(os.path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESC = '\n' + f.read()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

REQUIRED = ['maya', 'requests']

PACKAGES = ['regenmaschine']

ABOUT = dict()
with open(os.path.join(HERE, 'regenmaschine', '__version__.py'), 'r') as f:
    exec(f.read(), ABOUT)  # pylint: disable=exec-used

setup(
    name='regenmaschine',
    version=ABOUT['__version__'],
    description='A simple API for RainMachine sprinkler controllers',
    long_description=LONG_DESC,
    author='Aaron Bach',
    author_email='bachya1208@gmail.com',
    url='https://github.com/bachya/regenmaschine',
    packages=PACKAGES,
    install_requires=REQUIRED,
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'), )
