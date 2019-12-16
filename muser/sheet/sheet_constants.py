#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/sheet/sheet_constants.py       #
# Project: /williamye/program/pyxel_projects/muser/sheet                       #
# Created Date: Monday, December 2nd 2019, 07:48:59 pm                         #
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


class NoteType:
    NOTE = 0
    WAIT = 1
    TEMPO = 2
    FANCY = 3
    STOP_FANCY = 4

class NoteAction:
    IN = 0
    OUT = 1

# Length from the note to the center: l (px)
# Beat: b (beat)
# Time: t (ms)
# Beat Interval: s (ms / beat)
# t = b * s
# 
# Note Speed stores the time (beat)
"""
To calculate how many pixels per millisecond:
px/ms = l / t
"""
class NoteSpeed:
    SLOW = 2000
    MEDIUM = 1000
    FAST = 500

    @staticmethod
    def to_speed(length: int, time: int):
        return length / time
