#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game/playthrough/effect/move_effect.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game/playthrough/effect #
# Created Date: Thursday, June 4th 2020, 12:22:57 pm                           #
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


from game.playthrough.effect.base_effect import Effect
from sheet.gen.abs_output import StartMove


class Move:
    def __init__(self, pos1: tuple, pos2: tuple, offset: float,
                 time_length: float, object_identity: int):
        self.pos1 = pos1
        self.pos2 = pos2
        self.offset = offset
        self.time_length = time_length
        self.object_identity = object_identity
        self.started = False
        self.finish = False

    def get_current_pos(self, total_time: float):
        self.progress = self.get_progress(total_time)
        if self.progress >= 1:
            return self.pos2
        # From math stackexchange: https://math.stackexchange.com/a/1269705
        return ((1 - self.progress) * self.pos1[0] + self.progress * self.pos2[0],
                (1 - self.progress) * self.pos1[1] + self.progress * self.pos2[1])

    def get_progress(self, total_time: float):
        return (total_time - self.offset) / self.time_length

    def finished(self, total_time: float):
        return self.get_progress(total_time) >= 1


class MoveEffect(Effect):
    def __init__(self, move_note: StartMove):
        super().__init__(identity=move_note.identity)
        self.move_note = move_note
        self.note_prop = self.move_note.prop
        self.moves = [
            Move(
                element["pos1"],
                element["pos2"],
                self.note_prop["offset"] + element["offset"],
                element["time_length"],
                element["object_identity"])
            for element in self.note_prop["moves"]]

    def update(self, args, kwargs):
        from game.playthrough.effect.effect_controller import EffectController
        total_time: float = kwargs["total_time"]
        for move in self.moves:
            if move.finish:
                continue
            if total_time >= move.offset:
                move.started = True
            if total_time >= move.offset + move.time_length:
                move.finish = True
                continue
            if move.started and not move.finish:
                EffectController.pool[move.object_identity].note_prop["offset_pos"] = move.get_current_pos(
                    total_time)
                # print(f"Update: {EffectController.pool[move.object_identity].note_prop}")
        pass

    def draw(self, args, kwargs):
        pass
