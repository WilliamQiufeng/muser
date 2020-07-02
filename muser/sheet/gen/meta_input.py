#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/sheet/gen/meta_input.py        #
# Project: /williamye/program/pyxel_projects/muser/sheet/gen                   #
# Created Date: Monday, December 9th 2019, 06:42:26 pm                         #
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
#   Generate Sheet from meta                                                   #
#                                                                              #
*------------------------------------------------------------------------------*
'''


from sheet.gen.midi_converter import MidiToAbsSheet
from game_config import GLOB_CONFIG
import io
import json
import os


class MetaInput:
    @staticmethod
    def from_file(file_name):
        file = io.open(file_name, "r")
        return MetaInput(json.loads(file.read()))

    def __init__(self, meta):
        self.meta = meta

    def proc(self):
        sheets = []
        root: str = self.meta["root"].replace(
            "$asset_path", GLOB_CONFIG.assets.getSheets())
        # print(root)
        name = self.meta["name"]
        abs_output = os.path.join(root, self.meta["output"])
        for sheet in self.meta["sheets"]:
            # print(sheet)
            abs_midi = os.path.join(root, sheet["midi"])
            abs_music = os.path.join(root, sheet["music"])
            # print(abs_music)
            tempo_index = sheet["tempo_index"]
            indexes = sheet["indexes"]
            effect_pool = sheet["effect_pool"] if "effect_pool" in sheet.keys() else [
            ]
            effects = sheet["effects"] if "effects" in sheet.keys() else []
            music_offset = sheet["music_offset"] if "music_offset" in sheet.keys(
            ) else 2000
            operational_note = sheet["operational_note"] if "operational_note" in sheet.keys(
            ) else False
            mtas = MidiToAbsSheet(
                abs_midi, tempo_index, indexes, music_offset, False,
                operational_note)
            abs_sheet = mtas.to_abs_sheet({
                "author": sheet["author"],
                "music_author": sheet["music_author"],
                "version": sheet["version"],
                "name": name,
                "music": abs_music,
                "level": sheet["level"],
                "effect_pool": effect_pool,
                "effects": effects,
                "music_offset": music_offset
            })
            # print(abs_sheet)
            sheets.append(abs_sheet)
        io.open(abs_output, "w").write(json.dumps(sheets))
