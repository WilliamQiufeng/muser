#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/install.py                     #
# Project: /williamye/program/pyxel_projects/muser                             #
# Created Date: Wednesday, December 11th 2019, 07:57:05 am                     #
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


import io, os, sys
import json

print(sys.argv)
if not(len(sys.argv) > 1 and sys.argv[1] == "-n"):
    print("Packaging...")
    os.system("pyxelpackager main.py")
    print("Packaging Complete.")

install_path: str = input("Installation Path[path/n]: ")
if install_path == "n":
    print("No installation. Process complete")
    exit()
else:
    print("Copying Executable...")
    separator = "/"
    if os.path.exists("dist/main"):
        print("Unix installation")
        try:
            os.mkdir(f"{install_path}{separator}muser")
        except :
            print("Directory already exists")
        os.system(f"cp dist/main {install_path}{separator}muser{separator}muser")
    elif os.path.exists("dist/main.exe"):
        print("Non-unix installation")
        separator = "\\"
        try:
            os.mkdir(f"{install_path}{separator}muser")
        except:
            print("Directory already exists")
        os.system(f"cp dist/main.exe {install_path}{separator}muser{separator}Muser.exe")
    print("Copying Assets...")
    os.system(f"cp -r assets {install_path}{separator}muser{separator}assets")
    print("Generating Config...")
    config_file = io.open(f"{install_path}{separator}muser{separator}muser_config.json", "w")
    config_json = {
        "asset_path": f"{install_path}{separator}muser{separator}assets",
        "separator": separator
    }
    config_file.write(json.dumps(config_json))
    config_file.close()
    print("Installation Complete")
