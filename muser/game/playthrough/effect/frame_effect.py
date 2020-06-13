#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/muser/game/playthrough/effect/frame_effect.py #
# Project: /williamye/program/pyxel_projects/muser/muser/game/playthrough/effect #
# Created Date: Monday, December 16th 2019, 04:21:53 pm                        #
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


import pyxel, time, util
from game.playthrough.effect.base_effect import *
from game.constants import Constants
from sheet.gen.abs_output import *


class FrameEffect(Effect):
    def __init__(self, frame_note: StartFrame):
        super().__init__(identity=frame_note.identity)
        self.frame_note          = frame_note
        self.note_prop           = self.frame_note.prop
        self._frame              = self.note_prop["frame"]
        self.size_x, self.size_y = self.note_prop["size"]
        # Try to optimise
        self.frame = [
            (x, y, pix)
            for y in range(self.size_y)
            for x in range(self.size_x)
            for pix in [self._frame[y][x]]
            if pix != -1
        ]
        # print(self.frame_note.frame)
    def update(self, args, kwargs):
        pass

    @util.timeit(without=(-1, 30))
    # @numba.jit()
    def draw(self, args, kwargs):
        # pyxel.text(0, 250, f"{self.note_prop['offset_pos']}", 12)
        offset_pos_x, offset_pos_y = self.note_prop["offset_pos"]
        # If the frame is outside of the screen then don't draw
        if offset_pos_x > 256 or offset_pos_y > 256 or \
            offset_pos_x < (0 - self.size_x) or offset_pos_y < (0 - self.size_y):
                return None
        for x, y, pix in self.frame:
            pyxel.pset(offset_pos_x + x, offset_pos_y + y, pix)
