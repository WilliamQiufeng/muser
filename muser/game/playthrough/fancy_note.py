#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/muser/game/playthrough/fancy_note.py #
# Project: /williamye/program/pyxel_projects/muser/muser/game/playthrough      #
# Created Date: Friday, December 13th 2019, 03:27:59 pm                        #
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
from game.playthrough.effect.fancy_effect import *

class StartEffectNote(BaseNote):
    def __init__(self, effect_type: type, note):
        self.note = note
        self.effect_type: type = effect_type
        self.finished = False
        self.effect = effect_type(note)
        # Because access to notes will execute 'in' expr 2 times
        # For higher speed, I extracted it.
        self.identity = self.note.identity
        self.offset   = self.note.offset
    def update(self, total_time: int):
        if (not self.finished) and total_time >= self.offset:
            print(f"Effect Note {self.identity} In")
            EffectController.add_effect(self.effect)
            self.finished = True
    def __repr__(self):
        return f"StartEffect {self.effect_type} {self.identity} at {self.offset}"
    def draw(self):
        pass
class EndEffectNote(BaseNote):
    def __init__(self, end_fancy: EndEffect):
        self.end_fancy: EndEffect = end_fancy
        self.finished = False
        self.identity, self.offset = self.end_fancy.identity, self.end_fancy.offset
    def update(self, total_time: int):
        if (not self.finished) and total_time >= self.offset:
            # print(f"Effect note {self.identity} out")
            EffectController.remove_effect(self.identity)
            self.finished = True
    def __repr__(self):
        return f"EndFancyNote {self.identity} at {self.offset}"
    def draw(self):
        pass
