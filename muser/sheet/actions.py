#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/muser/sheet/actions.py         #
# Project: /williamye/program/pyxel_projects/muser/muser/sheet                 #
# Created Date: Friday, December 13th 2019, 01:21:46 pm                        #
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

from sheet.gen.abs_output import *
from sheet.sheet_constants import *

class Actions:
    @staticmethod
    def fromArgs(*args):
        note_type = int(args[0])
        if note_type == NoteType.NOTE:
            return AbsNote(*[float(x) for x in args[1:]], absolutified=True)
        elif note_type == NoteType.FANCY:
            return StartFancy(int(args[1]), [int(x) for x in args[2].split(";")], float(args[3]), int(args[4]),
                              [int(x) for x in args[5].split(";")], [int(x) for x in args[6].split(";")])
        elif note_type == NoteType.STOP_FANCY:
            return EndFancy(float(args[1]), int(args[2]))
        else:
            raise RuntimeError(f"Not supported: {args}")