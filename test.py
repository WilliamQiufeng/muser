from sheet.gen.meta_input import *
import os

root = "/williamye/program/pyxel_projects/muser/assets/sheets/"

file_list = os.listdir(root)
for file in file_list:
    if file.endswith(".sheetmeta"):
        MetaInput.from_file(root + file).proc()
