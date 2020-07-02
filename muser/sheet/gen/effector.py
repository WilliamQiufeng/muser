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


import sheet.gen.abs_output as ao
import copy


def add_effects(abs_notes: list, effect_pool: list, effects: list):
    # print(effect_pool)
    effect_vars = {}
    for effect_var in effect_pool:
        identity: int = int(effect_var["id"])
        offset_pos: list = effect_var["offset_pos"] if "offset_pos" in effect_var.keys() else [
            0, 0]
        effect = copy.copy(effect_var)
        effect.update({
            "identity": identity,
            "type": effect_var["type"],
            "offset_pos": offset_pos
        })
        effect_vars[identity] = effect
        # print(effect)
    # print(effect_vars)
    effect_list = []
    for effect in effects:
        identity: int = int(effect["id"])
        effect_var = effect_vars[identity]
        effect_type = effect_vars[identity]["type"]
        res = copy.copy(effect)
        res.update(effect_var)
        end = {
            "offset": effect["offset"] + effect["length"],
            "identity": identity
        }
        start_effect = getattr(ao, "Start" + effect_type.capitalize())(res)
        end_effect = ao.EndEffect(end)
        start_effect.do_func()
        effect_list.append(start_effect)
        effect_list.append(end_effect)
    res_list: list = abs_notes + effect_list
    res_list.sort(key=lambda n: n.offset)
    return res_list
