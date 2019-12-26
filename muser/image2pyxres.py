#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/image2pyxres.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser          #
# Created Date: Thursday, December 26th 2019, 03:37:40 pm                      #
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


import png, json
import pyxel

pyxel.init(1, 1)

print("Pyxel initialised")

filename = input("Image path: ")

reader = png.Reader(filename=filename)

out_res = input("Output pyxres file: ")
offset_pos = (int(input("Offset X: ")), int(input("Offset Y: ")))
pyxel.load(out_res)
pyxel.image(0, system=True).load(*offset_pos, filename)
pyxel.save(out_res)
print("Done")
