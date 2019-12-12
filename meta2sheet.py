from muser.game_config import *
from muser.sheet.gen.meta_input import *
import os

root = f"{GLOB_CONFIG.config['asset_path']}/sheets/"

file_list = os.listdir(root)
for file in file_list:
    if file.endswith(".sheetmeta"):
        MetaInput.from_file(root + file).proc()
