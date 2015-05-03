#!/usr/bin/env python
# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import setuptools

version = "0.2.1"

# @todo Add doctests and run them on Travis


setuptools.setup(
    name="MiniParse",
    version=version,
    description="Minimal, hence simple, parsing library, with a focus on clear error messages",
    author="Vincent Jacques",
    author_email="vincent@vincent-jacques.net",
    url="http://jacquev6.github.com/MiniParse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT LIcense",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    install_requires=["InteractiveCommandLine"],
    tests_require=["MockMockMock"],
    test_suite="MiniParse.tests",
    use_2to3=True,
    command_options={
        "build_sphinx": {
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "doc"),
        },
    },
)
