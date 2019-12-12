#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/sheet/note.py                  #
# Project: /williamye/program/pyxel_projects/muser/sheet                       #
# Created Date: Monday, December 2nd 2019, 08:09:21 pm                         #
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



from .sheet_constants import *
class Note:
    def __init__(self, type = NoteType.NOTE, length = 0, action = NoteAction.IN, speed = NoteSpeed.MEDIUM, tempo = 120):
        self.type = type
        self.length = length
        self.action = action
        self.speed = speed
        self.tempo = tempo