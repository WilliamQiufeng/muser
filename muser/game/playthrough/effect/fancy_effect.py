#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/muser/game/playthrough/effect/fancy_effect.py #
# Project: /williamye/program/pyxel_projects/muser/muser/game/playthrough/effect #
# Created Date: Saturday, December 14th 2019, 10:01:01 pm                      #
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

import pyxel
from game.playthrough.effect.base_effect import *
from game.constants import Constants
from sheet.gen.abs_output import *
class FancyEffect(Effect):
    
    def __init__(self, identity: int, fancy_note: StartFancy):
        super().__init__(identity=identity)
        self.fancy_note = fancy_note
        self.cur_color_index = 0
    
    def update(self, **kwargs):
        total_time: float = kwargs["total_time"]
        int_total_time = int(total_time)
        col_range = (int_total_time - self.fancy_note.offset) % (len(self.fancy_note.colors) * self.fancy_note.interval)
        for i in range(len(self.fancy_note.colors)):
            if i * self.fancy_note.interval <= col_range and col_range < (i + 1) * self.fancy_note.interval:
                self.cur_color_index = i
                # print(f"Color {self.colors[self.cur_color_index]}: {i * self.interval} <= {col_range} < {(i + 1) * self.interval}, {total_time}")
                break
    def draw(self, **kwargs):
        if self.fancy_note.colors[self.cur_color_index] != -1:
            pyxel.rect(*self.fancy_note.offset_pos, *self.fancy_note.size,
                        self.fancy_note.colors[self.cur_color_index])
