#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/muser/sheet/gen/effector.py    #
# Project: /williamye/program/pyxel_projects/muser/muser/sheet/gen             #
# Created Date: Friday, December 13th 2019, 02:46:44 pm                        #
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


from sheet.gen.abs_output import *

def add_effects(abs_notes: list, effects: list):
    effect_list = []
    for effect in effects:
        if effect["type"] == "fancy":
            identity: int = int(effect["id"])
            offset_pos: list = effect["offset_pos"] if "offset_pos" in effect.keys() else [0, 0]
            size: list = effect["size"] if "size" in effect.keys() else [256, 256]
            start_fancy = StartFancy(
                effect["offset"], effect["colors"], effect["interval"], identity, offset_pos=offset_pos, size=size)
            end_fancy = EndFancy(effect["offset"] + effect["length"], identity)
            effect_list.append(start_fancy)
            effect_list.append(end_fancy)
    res_list: list = abs_notes + effect_list
    res_list.sort(key=lambda n: n.offset)
    return res_list
