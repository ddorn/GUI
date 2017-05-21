#!/usr/bin/env python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
    
setup(
    name='Pygame GUI Lib',
    version='1.0a',
    description='Ease widgets for pygame',
    long_description=long_description,
    url="https://github.com/ddorn/GUI",
    author='Diego Dorn',
    author_email='diego.dorn@free.fr',
    packages=find_packages(),
    package_data={
        '': '*'
    }
)
