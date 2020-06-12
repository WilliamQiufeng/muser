from game_config import *
from sheet.gen.meta_input import *
import os

sheet_path = os.path.abspath(GLOB_CONFIG.assets.getSheets())

if os.path.islink(sheet_path):
    sheet_path = os.readlink(sheet_path)

print(f"Generating sheets under {sheet_path}")

file_list = os.listdir(sheet_path)
for file in file_list:
    if file.endswith(".sheetmeta"):
        MetaInput.from_file(os.path.join(sheet_path, file)).proc()
        