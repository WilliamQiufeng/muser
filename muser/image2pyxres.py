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

filename = input("Image name: ")

reader = png.Reader(filename=filename)
# read = list(reader.read())
# read[2] = list(read[2])
# color_code_res = []
# for row in read[2]:
#     arr = []
#     for i in range(int(read[0] / 3)):
#         color = row[i] * 65536 + row[i + 1] * 256 + row[i + 2]
#         diff = 2 ** 32
#         ind = -1
#         for palette_index in range(len(pyxel.DEFAULT_PALETTE)):
#             diff_cur = abs(color - pyxel.DEFAULT_PALETTE[palette_index])
#             if diff_cur < diff:
#                 diff = diff_cur
#                 ind = palette_index
#         arr.append(ind)
#     color_code_res.append(arr)

# print("Image read")

out_res = input("Output pyxres file: ")
offset_pos = (int(input("Offset X: ")), int(input("Offset Y: ")))
pyxel.load(out_res)
pyxel.image(0, system=True).load(*offset_pos, filename)
pyxel.save(out_res)
print("Done")
# size = (int(input("Size X: ")), int(input("Size Y: ")))

# image = pyxel.image(0, True)
# for y in range(size[1]):
#     for x in range(size[0]):
#         image.
