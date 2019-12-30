#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/frame2image.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser          #
# Created Date: Sunday, December 29th 2019, 03:47:24 pm                        #
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


import io
import pyxel
from game.frames import BitmapFrame
import json
import png


def int2rgb(n):
    b = n % 256
    g = int(((n-b)/256) % 256)      # always an integer
    r = int(((n-b)/256**2) - g/256)  # ditto
    return (r, g, b)

pyxel.init(1, 1)

frame_file = io.open(input("Input frame file: "))
frame_data = json.loads(frame_file.read())
frame_image= frame_data["frame"]
size = frame_data["size"]
print("Data loaded.")

substitution = frame_data["substitution"]

output_image_path = input("Output image path: ")
output_image = io.open(output_image_path, "wb")

writer = png.Writer(*size, greyscale=False)
writer.write(output_image, (
    [
        int2rgb(
            pyxel.DEFAULT_PALETTE[substitution[frame_image[y][x]]]
        )[i] for x in range(size[0]) for i in range(3)
    ] for y in range(size[1])
))
output_image.close()

print("Done")
