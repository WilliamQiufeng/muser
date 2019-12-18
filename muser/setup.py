#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/setup.py                       #
# Project: /williamye/program/pyxel_projects/muser                             #
# Created Date: Thursday, December 12th 2019, 12:53:39 pm                      #
# Author : Qiufeng54321                                                        #
# Email : williamcraft@163.com                                                 #
#                                                                              #
# Copyright (C) 2019  Qiufeng54321                                             #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
# You should have received a copy of the GNU General Public License            #
# along with this program.  If not, see <https://www.gnu.org/licenses/>.       #
# -----                                                                        #
# Description:                                                                 #
#                                                                              #
#                                                                              #
*------------------------------------------------------------------------------*
'''

import io
from setuptools import setup, find_packages

with open("../README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="muser",
    version="1.2.1.3",
    author="Qiufeng54321",
    author_email="williamcraft@163.com",
    description="A musical game made using pyxel",
    long_description = long_description,
    long_description_content_type='text/markdown',
    license="GPLv3",
    keywords="pyxel",
    url="https://github.com/Qiufeng54321/muser",
    install_requires=io.open("../requirements.txt", "r").read().split("\n"),
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'muser=muser:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
