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
import copy

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
                "identity": identity,
                "type": effect_var["type"],
                "colors": effect_var["colors"],
                "interval": effect_var["interval"],
                "offset_pos": offset_pos,
                "size": size
            }
            effect_vars[identity] = effect
        elif effect_var["type"] == "frame":
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
        elif effect_var["type"] == "move":
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
        elif effect_var["type"] == "criteria":
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
        if effect_type == "fancy":
            # start_fancy = StartFancy(
            #     effect["offset"], effect_var["colors"], effect_var["interval"], identity, offset_pos=effect_var["offset_pos"], size=effect_var["size"])
            # end_fancy = EndEffect(effect["offset"] + effect["length"], identity)
            start_fancy = StartFancy(res)
            end_fancy = EndEffect(end)
            effect_list.append(start_fancy)
            effect_list.append(end_fancy)
        elif effect_type == "frame":
            start_frame = StartFrame(res)
            start_frame.flatten_frame()
            end_frame = EndEffect(end)
            effect_list.append(start_frame)
            effect_list.append(end_frame)
        elif effect_type == "move":
            start_move = StartMove(res)
            end_move = EndEffect(end)
            effect_list.append(start_move)
            effect_list.append(end_move)
        elif effect_type == "criteria":
            start_criteria = StartCriteria(res)
            end_criteria = EndEffect(end)
            effect_list.append(start_criteria)
            effect_list.append(end_criteria)
    res_list: list = abs_notes + effect_list
    res_list.sort(key=lambda n: n.offset)
    return res_list
