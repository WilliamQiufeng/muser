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


class ArrowFrame(Frame):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
    INITIALS = [(0.5, 1), (0.5, 0), (1, 0.5), (0, 0.5)]
    OFFSETS = [(0, -16), (0, 0), (-16, 0), (0, 0)]

    def __init__(self, side: int = 0, width: int = 6, height: int = 6):
        self.side = side % 4
        self.width = width
        self.height = height
        self.col = Config.ARROW_COLORS[side]

    def draw(self, x, y):
        if self.side <= 1:  # The side is up or down
            x00 = x
            y00 = y + self.height / 2 - ArrowFrame.INITIALS[self.side][1]
            x01 = x + math.floor((self.width - 1) / 2)
            y01 = y00
            x02 = x01
            y02 = y - (ArrowFrame.INITIALS[self.side][1] - 1) * \
                self.height + (ArrowFrame.INITIALS[self.side][1] - 1)

            x10 = x + self.width - 1
            y10 = y00
            x11 = x + math.ceil((self.width - 1) / 2)
            y11 = y00
            x12 = x11
            y12 = y02

            pyxel.rect(x + self.width / 3 * 1, y, self.width /
                       3 * 1, self.height, self.col)
            pyxel.tri(x00, y00,
                      x01, y01,
                      x02, y02, self.col)
            pyxel.tri(x10, y10,
                      x11, y11,
                      x12, y12, self.col)
        else:
            x00 = x + self.width / 2 - ArrowFrame.INITIALS[self.side][0]
            y00 = y
            x01 = x00
            y01 = y + math.floor((self.height - 1) / 2)
            x02 = x - (ArrowFrame.INITIALS[self.side][0] - 1) * \
                self.width + (ArrowFrame.INITIALS[self.side][0] - 1)
            y02 = y01

            x10 = x00
            y10 = y + self.height - 1
            x11 = x00
            y11 = y + math.ceil((self.height - 1) / 2)
            x12 = x02
            y12 = y11

            pyxel.rect(x, y + self.height / 3 * 1, self.width,
                       self.height / 3 * 1, self.col)
            pyxel.tri(x00, y00,
                      x00, y01,
                      x02, y02,
                      self.col)
            pyxel.tri(x10, y10,
                      x11, y11,
                      x12, y12,
                      self.col)


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
                        new_image[y_o * scale_y + y_s][x_o *
                                                       scale_x + x_s] = placeholder
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
                        new_image[y_o * scale_y + y_s][x_o *
                                                       scale_x + x_s] = placeholder
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

