#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module sets up the package for the lib_gui"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(    
    name="lib_gui",
    author="Justin Furuness, Nick Lanotte",
    author_email="jfuruness@gmail.com",
    maintainer="Justin Furuness",
    maintainer_email="jfuruness@gmail.com",
    version="0.0.1",
    url="https://github.com/Mantis-Technologies/lib_gui.git",
    download_url='https://github.com/Mantis-Technologies/lib_gui.git',
    description="Controls the Kiosk for Mantis Technologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://mantistech.atlassian.net/jira/"
                       "software/projects/MTKD/boards/1?"
                       "assignee=5e7a90a679f5ad0c340506ba",
    },
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pytest',
        'pytest-qt',
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
            'lib_gui = lib_gui.__main__:main',
        ]},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
