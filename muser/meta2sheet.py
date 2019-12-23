from game_config import *
from sheet.gen.meta_input import *
import os
import argparse

argp = argparse.ArgumentParser()
argp.add_argument("-r", "--root", default='/Users/Shared/williamye/program/pyxel_projects/muser_sheeets')

args = argp.parse_args()

root = f"{args.root}/sheets/"

print(f"Generating sheets under {root}, root is {GLOB_CONFIG.assets.getSheets()}")

file_list = os.listdir(root)
for file in file_list:
    if file.endswith(".sheetmeta"):
        MetaInput.from_file(root + file).proc()
