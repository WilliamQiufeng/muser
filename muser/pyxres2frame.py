#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/pyxres2frame.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser          #
# Created Date: Tuesday, December 24th 2019, 07:26:39 am                       #
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


import pyxel, json.decoder
import io
import game_config as game_config
# import game.frame

pyxel.init(256, 256,
           caption="Muser", scale=48)

res_file = input("Resource File[path/n]: ")
if res_file == "n":
    res_file = f"{game_config.GLOB_CONFIG.assets.root}/resources.pyxres"
pyxel.load(res_file)
print("Res loaded")
image_index: int = int(input("Image index: "))
pos: tuple = (int(input("The offset x: ")), int(input("The offset y: ")))
display_pos: tuple = (int(input("Display offset x: ")), int(input("Display offset y: ")))
size: tuple = (int(input("Size width: ")), int(input("Size height: ")))
scale: tuple = (int(input("Scale X: ")), int(input("Scale Y: ")))
remove_color_input = input("Remove color: [0-15/n]: ")
remove_color: int = -1 if remove_color_input == "n" else int(remove_color_input)
substitution_col_to_key: tuple = tuple(" ABCDEFGHIJKLMNO")
substitution: dict = {}
# Substitution Col to Key Index
for sctk_i in range(len(substitution_col_to_key)):
    substitution[substitution_col_to_key[sctk_i]] = sctk_i
if remove_color != -1:
    substitution[substitution_col_to_key[remove_color]] = -1
res = {
    "id": 0,
    "type": "frame",
    "size": size,
    "offset_pos": display_pos
}


image: pyxel.Image = pyxel.image(image_index)

frame_image = [
    "".join(
        [
            substitution_col_to_key[image.get(pos[0] + x, pos[1] + y)]
            for x in range(size[0])
        ]
    ) 
    for y in range(size[1])
]

# scaled_frame = BitmapFrame.frameScaleUp(frame_image, *size, *scale)
scaled_frame = {
    "new_image": frame_image,
    "new_size": size
}

frame_image = ["".join(x) for x in scaled_frame["new_image"]]

res["size"] = scaled_frame["new_size"]

res["frame"] = frame_image

res["substitution"] = substitution

res_str = json.dumps(res, indent=4)

output = input("Output[file/stdout]: ")

if output == "stdout":
    print(res_str)
else:
    file = io.open(output, "w")
    file.write(res_str)
    file.close()
print("Done")
