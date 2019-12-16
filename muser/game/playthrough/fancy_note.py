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
from sheet.gen.abs_output import StartFancy, EndFancy
from game.playthrough.effect.effect_controller import *
from game.playthrough.effect.fancy_effect import *

class StartFancyNote(BaseNote):
    def __init__(self, fancy_note: StartFancy):
        self.fancy_note: StartFancy = fancy_note
        self.finished = False
        self.effect = FancyEffect(identity=self.fancy_note.identity, fancy_note=fancy_note)
    def update(self, total_time: int):
        if (not self.finished) and total_time >= self.fancy_note.offset:
            print("Fancy Note In")
            EffectController.add_effect(self.effect)
            self.finished = True
    def __repr__(self):
        return f"StartFancy {self.fancy_note.identity} at {self.fancy_note.offset}"
    def draw(self):
        pass
class EndFancyNote(BaseNote):
    def __init__(self, end_fancy: EndFancy):
        self.end_fancy: EndFancy = end_fancy
        self.finished = False
    def update(self, total_time: int):
        if (not self.finished) and total_time >= self.end_fancy.offset:
            print("Fancy note out")
            EffectController.remove_effect(self.end_fancy.identity)
            self.finished = True
    def __repr__(self):
        return f"EndFancyNote {self.end_fancy.identity} at {self.end_fancy.offset}"
    def draw(self):
        pass
