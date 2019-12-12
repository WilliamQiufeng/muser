from game_config import *
from sheet.gen.meta_input import *
import os
import argparse

argp = argparse.ArgumentParser()
argp.add_argument("-r", "--root", default=GLOB_CONFIG.config['asset_path'])

args = argp.parse_args()

root = f"{args.root}/sheets/"

file_list = os.listdir(root)
for file in file_list:
    if file.endswith(".sheetmeta"):
        MetaInput.from_file(root + file).proc()
