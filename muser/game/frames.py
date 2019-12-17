import pyxel
import math
class Frame:
    def __init__(self, x, y, width, height, image = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = 0
    def draw(self, x, y):
        pyxel.blt(x, y, self.image, self.x, self.y, self.width, self.height)
class ArrowFrame(Frame):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
    INITIALS = [(0.5, 1), (0.5, 0), (1, 0.5), (0, 0.5)]
    OFFSETS = [(0, -16), (0, 0), (-16, 0), (0, 0)]
    def __init__(self, side: int = 0, width: int = 6, height: int = 6, col = 5):
        self.side = side
        self.width = width
        self.height = height
        self.col = col
    def draw(self, x, y):
        if self.side <= 1: # The side is up or down
            x00 = x
            y00 = y + self.height / 2 - ArrowFrame.INITIALS[self.side][1]
            x01 = x + math.floor((self.width - 1) / 2)
            y01 = y00
            x02 = x01
            y02 = y - (ArrowFrame.INITIALS[self.side][1] - 1) * \
                self.height + (ArrowFrame.INITIALS[self.side][1] - 1)
            
            x10 = x + self.width - 1
            y10 = y00
            x11 = x + math.ceil((self.width - 1) / 2)
            y11 = y00
            x12 = x11
            y12 = y02
            
            pyxel.rect(x + self.width / 3 * 1, y, self.width / 3 * 1, self.height, self.col)
            pyxel.tri(x00, y00,
                      x01, y01,
                      x02, y02, self.col)
            pyxel.tri(x10, y10,
                      x11, y11,
                      x12, y12, self.col)
        else:
            x00 = x + self.width / 2 - ArrowFrame.INITIALS[self.side][0]
            y00 = y
            x01 = x00
            y01 = y + math.floor((self.height - 1) / 2)
            x02 = x - (ArrowFrame.INITIALS[self.side][0] - 1) * \
                self.width + (ArrowFrame.INITIALS[self.side][0] - 1)
            y02 = y01
            
            x10 = x00
            y10 = y + self.height - 1
            x11 = x00
            y11 = y + math.ceil((self.height - 1) / 2)
            x12 = x02
            y12 = y11
            
            pyxel.rect(x, y + self.height / 3 * 1, self.width, self.height / 3 * 1, self.col)
            pyxel.tri(x00, y00,
                      x00, y01,
                      x02, y02,
                      self.col)
            pyxel.tri(x10, y10,
                      x11, y11,
                      x12, y12,
                      self.col)
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
        UP_UNPRESSED, DOWN_UNPRESSED, UP_PRESSED, DOWN_PRESSED = (Frame(80 + 16 * x, 24, 16, 16) for x in range(4))
        PLAY_UNPRESSED = Frame(0, 64, 16, 16)
        PLAY_PRESSED = Frame(16, 64, 16, 16)
    class PlayThrough:
        # DIRECTIONS = [Frame(1 + x * 8, 5, 6, 6) for x in range(4)]
        DIRECTIONS = [ArrowFrame(x) for x in range(4)]
        ARROW_FADE = [Frame(56 + 8 * x, 4, 8, 8) for x in range(4)]
        INDICATOR_CIRCLE = Frame(32, 48, 32, 32)
        INDICATOR_RES = [Frame(x * 8, 16, 8, 8) for x in range(5)]
    class Result:
        S, A, B, C, D, F = (Frame(x * 16, 112, 16, 16) for x in range(6))
        
        @staticmethod
        def GRADES():
            return [
                Frames.Result.S,
                Frames.Result.A,
                Frames.Result.B,
                Frames.Result.C,
                Frames.Result.D,
                Frames.Result.F
            ]
