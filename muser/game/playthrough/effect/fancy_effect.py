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

import pyxel, util
from game.playthrough.effect.base_effect import *
from game.constants import Constants
from sheet.gen.abs_output import *
import numba
class FancyEffect(Effect):
    
    def __init__(self, fancy_note: StartFancy):
        super().__init__(identity=fancy_note.identity)
        self.fancy_note      = fancy_note
        self.cur_color_index = 0
        self.note_prop       = fancy_note.prop
    # @util.timeit(within=(1, -1))
    def update(self, args, kwargs):
        total_time: float = kwargs["total_time"]
        int_total_time    = int(total_time)
        col_range         = (int_total_time - self.note_prop["offset"]) % (len(self.note_prop["colors"]) * self.note_prop["interval"])
        for i in range(len(self.note_prop["colors"])):
            if i * self.note_prop["interval"] <= col_range and col_range < (i + 1) * self.note_prop["interval"]:
                self.cur_color_index = i
                # print(f"Color {self.colors[self.cur_color_index]}: {i * self.interval} <= {col_range} < {(i + 1) * self.interval}, {total_time}")
                break

    # @util.timeit(within=(1, -1))
    def draw(self, args, kwargs):
        if self.note_prop["colors"][self.cur_color_index] != -1:
            pyxel.rect(*self.note_prop["offset_pos"], *self.note_prop["size"],
                        self.note_prop["colors"][self.cur_color_index])
            