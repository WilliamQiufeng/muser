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


import importlib
import io, os, json
import assets as assets


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files or name in dirs:
            return os.path.join(root, name)
    return None

class GameConfig:
    def __init__(self):
        print(os.system("pwd"))
        self.config_path = find("muser_config.json", ".")
        print("Config path:", self.config_path)
        success: bool = True
        if self.config_path != None:
            try:
                self.config: dict = json.loads(io.open(self.config_path, "r").read())
            except:
                success = False
        if self.config_path == None or not success:
            self.config_path = os.path.join(os.path.abspath("."), "muser_config.json")
            self.config: dict = {}
    def proc(self):
        self.config["asset_path"]: str            = os.path.abspath(self.get("asset_path", default=find("assets", ".")))
        self.config["separator"]: str             = self.get("separator", default=os.path.sep)
        self.config["fps"]: int                   = self.get("fps", default=60)
        self.config["rel_music_offset"]: float    = self.get("rel_music_offset", default=0)
        self.config["full_screen"]: bool          = self.get("full_screen", default=False)
        self.config["control.up_arrow"]: bool     = self.get("control.up_arrow", default="w")
        self.config["control.down_arrow"]: bool   = self.get("control.down_arrow", default="s")
        self.config["control.left_arrow"]: bool   = self.get("control.left_arrow", default="a")
        self.config["control.right_arrow"]: bool  = self.get("control.right_arrow", default="d")
        self.config["control.up_arrow2"]: bool    = self.get("control.up_arrow2", default="i")
        self.config["control.down_arrow2"]: bool  = self.get("control.down_arrow2", default="k")
        self.config["control.left_arrow2"]: bool  = self.get("control.left_arrow2", default="j")
        self.config["control.right_arrow2"]: bool = self.get("control.right_arrow2", default="l")
        self.config["control.RD_arrow"]: bool     = self.get("control.RD_arrow", default="r")
        self.config["control.LD_arrow"]: bool     = self.get("control.LD_arrow", default="t")
        self.config["control.RU_arrow"]: bool     = self.get("control.RU_arrow", default="f")
        self.config["control.LU_arrow"]: bool     = self.get("control.LU_arrow", default="g")
        self.config["control.SEL_L"]: bool = self.get("control.SEL_L", default="left")
        self.config["control.SEL_R"]: bool = self.get("control.SEL_R", default="right")
        
        import pyxel
        self.controls = {
            key[8:]: getattr(pyxel, f"KEY_{self.config[key].upper()}")
            for key in self.config.keys()
            if key.startswith("control.")
        }
        print(self.controls)
        
        self.assets = assets.Assets(self.config["asset_path"], self.config["separator"])
    def save(self):
        io.open(self.config_path, "w").write(json.dumps(self.config, indent=4))
    def get(self, key, default = None):
        return self.config[key] if key in self.config.keys() else default

GLOB_CONFIG = GameConfig()
GLOB_CONFIG.proc()
GLOB_CONFIG.save()
