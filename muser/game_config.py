#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/game_config.py                 #
# Project: /williamye/program/pyxel_projects/muser                             #
# Created Date: Wednesday, December 11th 2019, 07:24:19 am                     #
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


import io, os, json
import assets as assets


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

class GameConfig:
    def __init__(self):
        print(os.system("pwd"))
        self.config_path = find("muser_config.json", ".")
        if self.config_path != None:
            self.config: dict = json.loads(io.open(self.config_path, "r").read())
        else:
            self.config_path = os.path.join(os.path.abspath("."), "muser_config.json")
            self.config: dict = {}
    def proc(self):
        self.asset_path: str = self.get("asset_path", default="./assets")
        self.separator: str = self.get("separator", default=os.path.sep)
        self.fps: int = self.get("fps", default=60)
        self.assets = assets.Assets(self.asset_path, self.separator)
    def save(self):
        self.config["asset_path"] = self.asset_path
        self.config["separator"] = self.separator
        self.config["fps"] = self.fps
        io.open(self.config_path, "w").write(json.dumps(self.config, indent=4))
    def get(self, key, default = None):
        return self.config[key] if key in self.config.keys() else default

GLOB_CONFIG = GameConfig()
GLOB_CONFIG.proc()
GLOB_CONFIG.save()
