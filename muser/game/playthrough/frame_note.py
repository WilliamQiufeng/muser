#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/muser/game/playthrough/frame_note.py #
# Project: /williamye/program/pyxel_projects/muser/muser/game/playthrough      #
# Created Date: Monday, December 16th 2019, 06:06:22 pm                        #
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


from game.playthrough.base_note import *
from sheet.gen.abs_output import StartFancy, EndEffect
from game.playthrough.effect.effect_controller import *
from game.playthrough.effect.frame_effect import *


class StartFrameNote(BaseNote):
    def __init__(self, frame_note: StartFrame):
        self.frame_note: StartFrame = frame_note
        self.finished = False
        self.effect = FrameEffect(
            identity=self.frame_note.identity, frame_note=frame_note)

    def update(self, total_time: int):
        if (not self.finished) and total_time >= self.frame_note.offset:
            print("Frame Note In")
            EffectController.add_effect(self.effect)
            self.finished = True

    def __repr__(self):
        return f"StartFrame {self.frame_note.identity} at {self.frame_note.offset}"

    def draw(self):
        pass
