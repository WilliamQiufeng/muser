#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game/frame.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game     #
# Created Date: Sunday, June 28th 2020, 06:36:35 pm                            #
# Author : Qiufeng54321                                                        #
# Email : williamcraft@163.com                                                 #
#                                                                              #
# Copyright (C) 2020  Qiufeng54321                                             #
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

import pyxel


class Frame:
    def __init__(self, x, y, width, height, image=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def draw(self, x, y):
        pyxel.blt(x, y, self.image, self.x, self.y, self.width, self.height)


class BitmapFrame(Frame):
    def __init__(self, width, height, image=[], substitution={}):
        super().__init__(0, 0, width, height, image=[
            list(x) if isinstance(x, str) else x for x in image])
        self.substitution = substitution
        self.optimize()

    @staticmethod
    def frameScaleUp(image: list, width: int = 16, height: int = 16, scale_x: int = 1, scale_y: int = 1):
        new_size = (width * scale_x, height * scale_y)
        new_image = [[' '] * new_size[0] for _ in range(new_size[1])]
        # y_o and x_o: y and x offsets
        for y_o in range(height):
            for x_o in range(width):
                placeholder = image[y_o][x_o]
                # y_s and x_s: y scale and x scale
                for y_s in range(scale_y):
                    for x_s in range(scale_x):
                        new_image[y_o * scale_y + y_s][x_o * scale_x + x_s] = placeholder
        return {
            "new_size": new_size,
            "new_image": new_image
        }

    def scaleUp(self, scale_x: int = 1, scale_y: int = 1):
        new_size = (self.width * scale_x, self.height * scale_y)
        new_image = [[' '] * new_size[0] for _ in range(new_size[1])]
        # y_o and x_o: y and x offsets
        for y_o in range(self.height):
            for x_o in range(self.width):
                placeholder = self.image[y_o][x_o]
                # y_s and x_s: y scale and x scale
                for y_s in range(scale_y):
                    for x_s in range(scale_x):
                        new_image[y_o * scale_y + y_s][x_o * scale_x + x_s] = placeholder
        self.width, self.height = new_size
        self.image = new_image
        self.optimize()
        return self

    def optimize(self):
        self._optimized = [
            (x, y, pix)
            for y in range(self.height)
            for x in range(self.width)
            for pix in [self.substitution[self.image[y][x]]]
            if pix != -1
        ]

    def draw(self, x, y, subs: dict = {}):
        # y_o and x_o: y and x offsets
        # for y_o in range(self.height):
        #     for x_o in range(self.width):
        #         col = self.substitution[self.image[y_o][x_o]]
        #         if col != -1:
        #             pyxel.pset(x + x_o, y + y_o, col)
        for x_o, y_o, pix in self._optimized:
            pyxel.pset(x + x_o, y + y_o,
                       subs[pix] if pix in subs.keys() else pix)

    @staticmethod
    def from_pyxel(pos, size, *, remove_color=0, image_index=0, scale=(1, 1)):
        substitution_col_to_key: tuple = tuple(" ABCDEFGHIJKLMNO")
        substitution: dict = {}
        # Substitution Col to Key Index
        for sctk_i in range(len(substitution_col_to_key)):
            substitution[substitution_col_to_key[sctk_i]] = sctk_i
        if remove_color != -1:
            substitution[substitution_col_to_key[remove_color]] = -1
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

        scaled_frame = BitmapFrame(
            *size, frame_image, substitution).scaleUp(*scale)
        return scaled_frame

    def __repr__(self):
        return '\n'.join([','.join(x) for x in self.image])
