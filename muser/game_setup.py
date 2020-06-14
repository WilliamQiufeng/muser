#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game_setup.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser          #
# Created Date: Sunday, June 14th 2020, 02:11:13 pm                            #
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


import util
import os, io, sys, time

def sprint(text):
    return input(text)

sprint("----Game setup wizard----")
sprint("Welcome to the installation setup wizard for muser.\n")
sprint("The game consists of two parts: game itself and the music sheets which is the 'maps' of the game.")
sprint("It is optional to have default sheets installed. Note that if there are no sheets installed")
sprint("on run, The game will crash until you have installed at least one sheet.")

sprint("This setup wizard will setup the following things (All optional)")
sprint("+ Required libraries (The game needs them to properly work)")
sprint("+ Game config ('muser_config.json' used for options for preferences and controls)")
sprint("+ Default sheets (Sheets made along with the game but is separated in case you don't want them)")

sprint("Setup will start now.")

install_required_libraries : bool = sprint("1. Do you want to install the required libraries? [any/n]") != "n"
install_game_config        : bool = sprint("2. Do you want to install the game config? [any/n]")        != "n"
install_default_sheets     : bool = sprint("3. Do you want to install the default sheet pack? [any/n]") != "n"

print("Got it.")

if install_required_libraries:
    print("Installing required libraries...")
    util.pip_install("pyxel>=1.4 mido pyglet pynput".split(" "))
    print("Library installation complete.")

if install_game_config:
    print("Writing game_config (Will only create files if not exist or non-existent options)")
    import game_config
    print(game_config.GLOB_CONFIG.config)
    print("Game config written.")
    
# TODO: Install default sheets

print("Setup wizard complete. You may now try the game by running main.py!")