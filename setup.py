#!/usr/bin/env python

# Always prefer setuptools over distutils
import os

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# I really prefer Markdown to reStructuredText.  PyPi does not.  This allows me
# to have things how I'd like, but not throw complaints when people are trying
# to install the package and they don't have pypandoc or the README in the
# right place.
try:
   import pypandoc
   pypandoc.download_pandoc()
   print(os.curdir)
   print(here)
   print(os.listdir(os.curdir))
   try:
       long_description = pypandoc.convert('README.md', 'rst')
   except RuntimeError:
       try:
           long_description = pypandoc.convert('readme.md', "rst")
       except RuntimeError:
           long_description=''
           print('FUCK THE DESCRIPTION')
except (IOError, ImportError):
   long_description = ''


setup(
    name='PygameGUILib',
    version='0.4a4',
    description='widgets for pygame wit ease',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='pygame widget widgets gui',
    url="https://github.com/ddorn/GUI",
    author='Diego Dorn',
    author_email='diego.dorn@free.fr',
    packages=find_packages(),
    package_data={
        '.': 'README.*'
    },
    install_requires=['pygame'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
