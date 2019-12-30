#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/pyxres2image.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser          #
# Created Date: Thursday, December 26th 2019, 04:00:08 pm                      #
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


import png
import pyxel
import io
from itertools import chain


res_path = input(
    "Path to resource[/Users/Shared/williamye/program/pyxel_projects/muser/muser/assets/buf.pyxres]: ")
if res_path.isspace() or len(res_path) == 0:
    res_path = "/Users/Shared/williamye/program/pyxel_projects/muser/muser/assets/buf.pyxres"
print(res_path)

def int2rgb(n):
    b = n % 256
    g = int(((n-b)/256) % 256)      # always an integer
    r = int(((n-b)/256**2) - g/256)  # ditto
    return (r, g, b)

pyxel.init(1, 1)
print("Pyxel initialised")
pyxel.load(res_path)

print("Res loaded")

image_index = int(input("Image Index: "))
offset_pos = (int(input("Offset X: ")), int(input("Offset Y: ")))
size = (int(input("Size X: ")), int(input("Size Y: ")))


out_path = input("Output Image Path: ")
out = io.open(out_path, "wb")

writer = png.Writer(*size, greyscale=False)
writer.write(out, (
    [
        int2rgb(
            pyxel.DEFAULT_PALETTE[pyxel.image(
                image_index).data[y + offset_pos[1]][x + offset_pos[0]]]
        )[i] for x in range(size[0]) for i in range(3)
    ] for y in range(size[1])
))
out.close()

print("Done")
