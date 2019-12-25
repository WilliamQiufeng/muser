import pyxel
from sheet.reader import sheet_reader
from game.constants import *
from game.config import *
from game.casts import *
import traceback

class Muser:
    def __init__(self):
        pyxel.run(self.update, self.draw)
    def update(self):
        try: 
            if Config.CAST.is_finished():
                Config.CAST = Config.CAST.next_cast()
            Config.CAST.update()
        except BaseException as e:
            print(e)
            traceback.print_exc()
            exit()
    def draw(self):
        Config.CAST.clear_screen()
        Config.CAST.draw()
Muser()
