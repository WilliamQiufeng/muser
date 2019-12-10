from .rel_input import *

def gen_init():
    process = SourceSheetInput("/williamye/program/pyxel_projects/muser/test/test.data")
    process.process_all()
    print(vars(process))
    print(process.to_abs())
    print("End")