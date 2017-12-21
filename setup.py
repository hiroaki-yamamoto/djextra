#!/usr/bin/env python
# coding=utf-8
"""Setup script."""

import sys
from setuptools import setup, find_packages

dependencies = ["django>=1.11"]
name = "djextra"
desc = "Additional Functions for Django"
license = "MIT"
url = "https://github.com/hiroaki-yamamoto/djextra"
keywords = "Django"
version = "[VERSION]"

author = "Hiroaki Yamamoto"
author_email = "hiroaki@hysoftware.net"

if sys.version_info < (2, 7):
    raise RuntimeError("Not supported on earlier then python 2.7.")

try:
    with open('README.rst') as readme:
        long_desc = readme.read()
except Exception:
    long_desc = None

setup(
    name=name,
    version=version,
    description=desc,
    long_description=long_desc,
    packages=find_packages(exclude=["tests"]),
    install_requires=dependencies,
    zip_safe=False,
    author=author,
    author_email=author_email,
    license=license,
    keywords=keywords,
    url=url,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 1.11",
    ]
)
