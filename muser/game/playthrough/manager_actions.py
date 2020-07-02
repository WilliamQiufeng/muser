#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/muser/game/playthrough/manager_actions.py #
# Project: /williamye/program/pyxel_projects/muser/muser/game/playthrough      #
# Created Date: Friday, December 13th 2019, 03:24:05 pm                        #
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


import sheet.gen.abs_output as note_types
from game.playthrough.note import PositionedNote
# They are not unused, they are accessed through globals()
# flake8: noqa: F401
from game.playthrough.effect.frame_effect import FrameEffect
from game.playthrough.effect.move_effect import MoveEffect
from game.playthrough.effect.criteria_effect import CriteriaEffect
from game.playthrough.effect.fancy_effect import FancyEffect
from game.playthrough.fancy_note import StartEffectNote, EndEffectNote


class ManagerActions:
    @staticmethod
    def from_note(note):
        note_type: str = type(note).__name__
        if isinstance(note, note_types.AbsNote):
            return PositionedNote(note)
        elif isinstance(note, note_types.EndEffect):
            return EndEffectNote(note)
        elif hasattr(note_types, note_type):
            # note_type[5:] : Remove 'Start' at type name.
            return StartEffectNote(globals()[note_type[5:] + "Effect"], note)
        else:
            return note
