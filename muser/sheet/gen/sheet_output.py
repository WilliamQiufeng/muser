#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/sheet/gen/sheet_output.py      #
# Project: /williamye/program/pyxel_projects/muser/sheet/gen                   #
# Created Date: Tuesday, December 10th 2019, 01:23:02 pm                       #
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
from muser.sheet.gen.abs_output import *
class SheetOutput:
    def __init__(self, sheets: list):
        self.sheets = sheets
    def write(self, filename):
        file = io.open(filename, "w")
        file.write("|".join([str(sheet) for sheet in self.sheets]))
        
