#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game/playthrough/effect/criteria_effect.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game/playthrough/effect #
# Created Date: Tuesday, June 9th 2020, 10:21:09 am                            #
# Author : Qiufeng54321                                                        #
# Email : williamcraft@163.com                                                 #
#                                                                              #
# Copyright (C) 2020  Qiufeng54321                                             #
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
import util
from game.playthrough.effect.base_effect import *
from game.constants import Constants
from sheet.gen.abs_output import *
import numba
import game.playthrough.criteria_manager as cm


class CriteriaEffect(Effect):

    def __init__(self, criteria_note: StartCriteria):
        super().__init__(identity=criteria_note.identity)
        self.criteria_note = criteria_note
        self.note_prop = criteria_note.prop
        self.lock_effect_identity: int = self.note_prop["lock_effect_identity"]
        self.sides: list = self.note_prop["sides"]
        self.done: bool = False
    # @util.timeit(within=(1, -1))

    def update(self, args, kwargs):
        if self.done:
            return None
        cm.set_criteria(self.lock_effect_identity, self.sides)
        self.done = True

    # @util.timeit(within=(1, -1))
    def draw(self, args, kwargs):
        pass
