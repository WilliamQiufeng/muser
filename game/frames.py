import pyxel
class Frame:
    def __init__(self, x, y, width, height, image = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = 0
    def draw(self, x, y):
        pyxel.blt(x, y, self.image, self.x, self.y, self.width, self.height)
class Frames:
    class Intro:
        EMPTY = [Frame(80, 136, 79, 16)]
        TITLE_PRE = EMPTY * 20
        TITLE_FADEIN = [Frame(0, 136 + 16 * x, 79, 16) for x in range(0, 5)]
        TITLE_STAY = [Frame(0, 200, 79, 16)] * 100
        TITLE_FADEOUT = TITLE_FADEIN[::-1]
        TITLE = TITLE_PRE + TITLE_FADEIN + TITLE_STAY + TITLE_FADEOUT
        AUTHOR_FADEIN = [Frame(80, 152 + 16 * x, 79, 16) for x in range(0, 4)]
        AUTHOR_STAY = [Frame(80, 200, 79, 16)] * 100
        AUTHOR_FADEOUT = AUTHOR_FADEIN[::-1] + EMPTY
        AUTHOR = AUTHOR_FADEIN + AUTHOR_STAY + AUTHOR_FADEOUT
        WHOLE = TITLE + AUTHOR
    class LevelSelection:
        LEFT_UNPRESSED = Frame(16, 24, 16, 16)
        LEFT_PRESSED = Frame(48, 24, 16, 16)
        RIGHT_UNPRESSED = Frame(32, 24, 16, 16)
        RIGHT_PRESSED = Frame(64, 24, 16, 16)
        PLAY_UNPRESSED = Frame(0, 64, 16, 16)
        PLAY_PRESSED = Frame(16, 64, 16, 16)
    class PlayThrough:
        DIRECTIONS = [Frame(1 + x * 8, 5, 6, 6) for x in range(4)]
        INDICATOR_CIRCLE = Frame(32, 48, 32, 32)
        INDICATOR_RES = [Frame(x * 8, 16, 8, 8) for x in range(5)]
