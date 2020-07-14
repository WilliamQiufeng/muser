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
import os
import sys


def sprint(text):
    return print(text)


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

install_required_libraries: bool = input(
    "1. Do you want to install the required libraries? [any/n]") != "n"
install_game_config: bool = input(
    "2. Do you want to install the game config? [any/n]") != "n"
install_default_sheets: bool = input(
    "3. Do you want to install the default sheet pack? [any/n]") != "n"

print("Got it.")

if install_required_libraries:
    print("Installing required libraries...")
    util.pip_install(
        "--user pyxel>=1.4 mido pyglet pynput requests".split(" "))
    print("Library installation complete.")

if install_game_config:
    print("Writing game_config (Will only create files if not exist or non-existent options)")
    import game_config
    print(game_config.GLOB_CONFIG.config)
    print("Game config written.")

# TODO: Install default sheets
if install_default_sheets:
    try:
        import requests
    except Exception:
        print("[ERROR] 'requests' lib not installed. Please install this lib.")
        exit()
    # git cat-file -p `git describe --abbrev=0` | tail -n +6
    # expands into:
    #   $a = git describe --abbrev=0
    #   git cat-file -p $a > .tmpdesc
    #   tail -n +6 .tmpdesc
    #   rm .tmpdesc

    # command = ['git', 'describe', '--abbrev=0']
    # latest_tag = util.cmd(command)[0][:-1]
    # # tag_desc = util.cmd(["git", "cat-file", "-p", latest_tag])[0]
    # tag_desc = util.cmd(["git", "cat-file", "-p", util.version])[0]
    # tmp = io.open('.tmpdesc', 'w')
    # tmp.write(tag_desc)
    # tmp.close()
    # message = util.cmd(['tail', '-n', '+6', '.tmpdesc'])[0]
    # os.remove('.tmpdesc')

    # links = util.find_links(message)
    # print("Links found:", links)
    # print("Choosing the first link:", links[0])
    origin_link = "https://api.github.com/repos/Qiufeng54321/muser/releases/latest"

    mirror_link = "https://main.williamcraft.workers.dev/?target=get_latest_version"
    # retrieving data from the URL using get method
    path = input("Do you want to download or use you own? [path/n]: ")
    if path == "n":
        link = mirror_link if input(
            "Do you want to use a mirror link? [any/n]:") != "n" else origin_link
        if link == origin_link:
            print("Getting latest sheets asset link from github...")
            import json
            latest_release = json.loads(requests.get(origin_link).text)
            link = latest_release["assets"][0]["browser_download_url"]
        print(f"Using link: {link}")
        r = requests.get(link, stream=True)
        path = ".muser_sheets.zip"
        print("Downloading " + link + " to " + path)
        with open(path, 'wb') as f:
            # giving a name and saving it in any required format
            # opening the file in write mode
            size = int(r.headers['content-length'])
            print("File size: " + util.humanbytes(size))
            written = 0
            last_percentage: int = 0
            sys.stdout.write("|" + ' ' * 100 + "| 0%       0.0 B")
            sys.stdout.flush()
            for chunk in r.iter_content(chunk_size=512):
                f.write(chunk)
                written += len(chunk)
                percentage: int = int(written / size * 100)
                if percentage != last_percentage:
                    sys.stdout.write('\b' * 117)
                    sys.stdout.write("|" + ('-' * (percentage - 1) + '>' if percentage > 0 else '') + ' ' * (100 - percentage) + "| ")
                    sys.stdout.write((str(percentage) + "%").ljust(4))
                    sys.stdout.write(util.humanbytes(written).rjust(10))
                    sys.stdout.flush()
                    last_percentage = percentage
                else:
                    sys.stdout.write('\b' * 10)
                    sys.stdout.write(util.humanbytes(written).rjust(10))
                    sys.stdout.flush()
            print("Sheets downloaded.")
    path = os.path.abspath(path)
    print("Extracting " + path + " to '.muser_sheets'...")
    util.unzip_files(path, ".muser_sheets")
    print("Extracted.")

    print("Copying to assets...")
    sheet_install_path: str = input(
        "Where do you want to install the sheets[path/n/empty(../../muser_sheets/)]: ")
    if sheet_install_path == "n" or sheet_install_path.isspace() or len(
            sheet_install_path) == 0 or not os.path.exists(sheet_install_path):
        sheet_install_path = "../../muser_sheets/"
    sheet_install_path = os.path.abspath(sheet_install_path)
    import shutil
    os.makedirs(sheet_install_path, exist_ok=True)
    extracted = ".muser_sheets/"
    util.copy_multiple([
        os.path.join(extracted, name)
        for name in os.listdir(extracted)
    ], sheet_install_path)
    print("Copy complete. Removing temp extracted directory...")
    shutil.rmtree(".muser_sheets/")
    print("Removed temp extracted directory")

    print("Linking to assets/sheets...")
    target_dir = "assets/sheets"
    if os.path.abspath(sheet_install_path) != os.path.abspath(target_dir):
        if os.path.exists(target_dir):
            remove_origin: bool = input(
                "Do you want to remove assets/sheets? [any/n]: ") != "n"
            if remove_origin:
                if os.path.islink(target_dir):
                    os.unlink(target_dir)
                else:
                    shutil.rmtree(target_dir)
        os.symlink(sheet_install_path, target_dir, True)
    print("Linked " + sheet_install_path + " -> " + target_dir)

    print("Generating sheets...")
    import meta2sheet
    meta2sheet.generate()
    print("Generation complete.")


print("Setup wizard complete. You may now try the game by running main.py!")
print("To run main.py: ")
print("Method 1: Double click main.py to run it")
print("Method 2: Shell: ")
cwd = os.path.dirname(os.path.abspath(
    __file__)) if __file__ is not None else os.curdir
us_len: int = len(cwd) + 3
if us_len < 20:
    us_len = 20
print(" ___" + "_" * us_len + "_ ")
print("|   " + " " * us_len + " |")
print("| > " + ("cd " + cwd).ljust(us_len) + " |")
print("| > " + "python main.py".ljust(us_len) + " |")
print("|___" + "_" * us_len + "_|")
