#!python
"""rippy setup file, used to install the rippy package.

   This package consists of library to assist in the generation of rst
   documentation

"""
from setuptools import setup, find_packages
import sys
VERSION = open('version.txt').read().strip()

scripts = []

setup(name='rippy',
      version=VERSION,
      description='reStructuredText library to generate rst documentation',
      author='Andrew Sawyers',
      author_email='andrew@sawdog.com',
      license='Modified BSD License',
      long_description = open('README.rst').read(),
      keywords = 'reST reStructuredText documentation library',
      url = 'https://github.com/sawdog/rippy',
      packages = find_packages(),
      py_modules = [],
      zip_safe = False,
      entry_points = {},
      classifiers = [f.strip() for f in """
      Development Status :: 3 - Alpha
      Environment :: Other Environment
      Intended Audience :: Developers
      License :: OSI Approved :: BSD
      Operating System :: OS Independent
      Programming Language :: Python
      Topic :: Documentation
      Topic :: Software Development :: Documentation
      Topic :: Software Development :: Libraries :: Python Modules
      Topic :: Utilities""".splitlines() if f.strip()],
      scripts = scripts,
      install_requires = ['nose'],
)

