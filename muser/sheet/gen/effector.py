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

def add_effects(abs_notes: list, effect_pool: list, effects: list):
    # print(effect_pool)
    effect_vars = {}
    for effect_var in effect_pool:
        if effect_var["type"] == "fancy":
            identity: int = int(effect_var["id"])
            offset_pos: list = effect_var["offset_pos"] if "offset_pos" in effect_var.keys() else [
                0, 0]
            size: list = effect_var["size"] if "size" in effect_var.keys() else [
                256, 256]
            effect = {
                "type": effect_var["type"],
                "colors": effect_var["colors"],
                "interval": effect_var["interval"],
                "offset_pos": offset_pos,
                "size": size
            }
            effect_vars[identity] = effect
        elif effect_var["type"] == "frame":
            identity: int = int(effect_var["id"])
            size: list = effect_var["size"]
            frame_list: list = effect_var["frame"]
            subst: dict = effect_var["substitution"]
            offset_pos: list = effect_var["offset_pos"] if "offset_pos" in effect_var.keys() else [
                0, 0]
            effect = {
                "type": effect_var["type"],
                "size": size,
                "frame": frame_list,
                "substitution": subst,
                "offset_pos": offset_pos
            }
            effect_vars[identity] = effect
            # print(effect)
    # print(effect_vars)
    effect_list = []
    for effect in effects:
        identity: int = int(effect["id"])
        effect_type = effect_vars[identity]["type"]
        if effect_type == "fancy":
            effect_var = effect_vars[identity]
            start_fancy = StartFancy(
                effect["offset"], effect_var["colors"], effect_var["interval"], identity, offset_pos=effect_var["offset_pos"], size=effect_var["size"])
            end_fancy = EndEffect(effect["offset"] + effect["length"], identity)
            effect_list.append(start_fancy)
            effect_list.append(end_fancy)
        elif effect_type == "frame":
            effect_var = effect_vars[identity]
            start_frame = StartFrame(effect["offset"], effect_var["size"], effect_var["frame"], effect_var["substitution"], effect_var["offset_pos"], identity)
            end_frame = EndEffect(effect["offset"] + effect["length"], identity)
            effect_list.append(start_frame)
            effect_list.append(end_frame)
    res_list: list = abs_notes + effect_list
    res_list.sort(key=lambda n: n.offset)
    return res_list
