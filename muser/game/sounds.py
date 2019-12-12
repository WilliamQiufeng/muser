#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/game/sounds.py                 #
# Project: /williamye/program/pyxel_projects/muser/game                        #
# Created Date: Tuesday, December 10th 2019, 06:28:33 pm                       #
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


import pygame.mixer_music
import game_config as game_config
pygame.mixer.init()
class Sound:
    def __init__(self, path):
        self.path = path
    def play(self):
        try:
            pygame.mixer.music.load(self.path)
            pygame.mixer.music.play()
        except:
            print("Error loading sound")

class Sounds:
    class Grade:
        A = Sound(
            game_config.GLOB_CONFIG.assets.get("sounds/A.flac"))
        C = Sound(
            game_config.GLOB_CONFIG.assets.get("assets/sounds/C.flac"))
