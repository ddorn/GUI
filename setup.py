#!/usr/bin/env python

# Always prefer setuptools over distutils
import os

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open('readme.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PygameGUILib',
    version='0.3a1',
    description='widgets for pygame wit ease',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='pygame widget widgets gui',
    url="https://github.com/ddorn/GUI",
    author='Diego Dorn',
    author_email='diego.dorn@free.fr',
    packages=find_packages(),
    package_data={
        '': '*'
    },
    install_requires=['pygame'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
