import pyxel
from sheet.reader import sheet_reader
from game.constants import *
from game.config import *
from game.casts import *

class Muser:
    def __init__(self):
        pyxel.run(self.update, self.draw)
    def update(self):
        if Config.CAST.is_finished():
            Config.CAST = Config.CAST.next_cast()
        Config.CAST.update()
    def draw(self):
        pyxel.cls(0)
        Config.CAST.draw()
Muser()
