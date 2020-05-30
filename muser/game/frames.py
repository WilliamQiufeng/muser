import pyxel
import math
from game.config import *
class Frame:
    def __init__(self, x, y, width, height, image = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
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
    def __init__(self, side: int = 0, width: int = 6, height: int = 6):
        self.side = side
        self.width = width
        self.height = height
        self.col = Config.ARROW_COLORS[side]
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

class BitmapFrame(Frame):
    def __init__(self, width, height, image=[], substitution={}):
        super().__init__(0, 0, width, height, image=[list(x) if isinstance(x, str) else x for x in image])
        self.substitution = substitution
    @staticmethod
    def frameScaleUp(image: list, width: int = 16, height: int = 16, scale_x: int = 1, scale_y: int = 1):
        new_size = (width * scale_x, height * scale_y)
        new_image = [[' '] * new_size[0] for _ in range(new_size[1])]
        # y_o and x_o: y and x offsets
        for y_o in range(height):
            for x_o in range(width):
                placeholder = image[y_o][x_o]
                # y_s and x_s: y scale and x scale
                for y_s in range(scale_y):
                    for x_s in range(scale_x):
                        new_image[y_o * scale_y + y_s][x_o * scale_x + x_s] = placeholder
        return {
            "new_size": new_size,
            "new_image": new_image
        }
    def scaleUp(self, scale_x: int = 1, scale_y: int = 1):
        new_size = (self.width * scale_x, self.height * scale_y)
        new_image = [[' '] * new_size[0] for _ in range(new_size[1])]
        # y_o and x_o: y and x offsets
        for y_o in range(self.height):
            for x_o in range(self.width):
                placeholder = self.image[y_o][x_o]
                # y_s and x_s: y scale and x scale
                for y_s in range(scale_y):
                    for x_s in range(scale_x):
                        new_image[y_o * scale_y + y_s][x_o * scale_x + x_s] = placeholder
        self.width, self.height = new_size
        self.image = new_image
        return self
    def draw(self, x, y):
        # y_o and x_o: y and x offsets
        for y_o in range(self.height):
            for x_o in range(self.width):
                col = self.substitution[self.image[y_o][x_o]]
                if col != -1:
                    pyxel.pset(x + x_o, y + y_o, col)
    def __repr__(self):
        return '\n'.join([','.join(x) for x in self.image])

class Frames:
    class Init:
        DIRECTORY = Frame(0, 216, 16, 16)
        FILE = Frame(16, 216, 16, 16)
        BACK = Frame(32, 216, 16, 16)
        ENTER = Frame(48, 216, 16, 16)
    class Intro:
        EMPTY = [Frame(80, 136, 79, 16)]
        TITLE_PRE = EMPTY * 20
        TITLE_FADEIN = [Frame(0, 136 + 16 * x, 79, 16) for x in range(0, 5) for _ in range(int(game_config.GLOB_CONFIG.config["fps"] / 15))]
        TITLE_STAY = [Frame(0, 200, 79, 16)] * \
            int(game_config.GLOB_CONFIG.config["fps"] * 2)
        TITLE_FADEOUT = TITLE_FADEIN[::-1]
        TITLE = TITLE_PRE + TITLE_FADEIN + TITLE_STAY + TITLE_FADEOUT
        AUTHOR_FADEIN = [Frame(80, 152 + 16 * x, 79, 16) for x in range(0, 4)
                         for _ in range(int(game_config.GLOB_CONFIG.config["fps"] / 15))]
        AUTHOR_STAY = [Frame(80, 200, 79, 16)] * \
            int(game_config.GLOB_CONFIG.config["fps"] * 2)
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
        # INDICATOR_CIRCLE = Frame(32, 48, 32, 32)
        INDICATOR_CIRCLE = BitmapFrame(32, 32, [
            "             H    H             ",
            "             H    H             ",
            "                                ",
            "                                ",
            "             H    H             ",
            "             H    H             ",
            "             H    H             ",
            "       HHHHHHHHHHHHHHHHHH       ",
            "       HHHHH        HHHHH       ",
            "       HH              HH       ",
            "       HH              HH       ",
            "       HH              HH       ",
            "HH  HHHH                H       ",
            "       H                HHHH  HH",
            "       H                H       ",
            "       H                H       ",
            "       H                H       ",
            "       H                H       ",
            "       H                HHHH  HH",
            "HH  HHHH                H       ",
            "       HH              HH       ",
            "       HH              HH       ",
            "       HH              HH       ",
            "       HHHHH        HHHHH       ",
            "       HHHHHHHHHHHHHHHHHH       ",
            "             H    H             ",
            "             H    H             ",
            "             H    H             ",
            "                                ",
            "                                ",
            "             H    H             ",
            "             H    H             "
        ], {
            " ": -1,
            "H": 8,
        })
        # INDICATOR_RES = [Frame(x * 8, 16, 8, 8) for x in range(5)]
        INDICATOR_SCALE = (2, 2)
        INDICATOR_RES = [
            BitmapFrame(5, 6, [
                ' OOO ',
                'O   O',
                'O   O',
                'OOOO ',
                'O    ',
                'O    '
            ], {
                ' ': -1,
                'O': 8
            }).scaleUp(*INDICATOR_SCALE),
            BitmapFrame(5, 6, [
                ' OOO ',
                'O   O',
                'O    ',
                'O OOO',
                'O   O',
                ' OOOO'
            ], {
                ' ': -1,
                'O': 12
            }).scaleUp(*INDICATOR_SCALE),
            BitmapFrame(5, 6, [
                ' OOO ',
                'O   O',
                'OOOO ',
                'O   O',
                'O   O',
                'OOOO '
            ], {
                ' ': -1,
                'O': 13
            }).scaleUp(*INDICATOR_SCALE),
            BitmapFrame(5, 6, [
                'O   O',
                'OO OO',
                'O O O',
                'O O O',
                'O   O',
                'O   O'
            ], {
                ' ': -1,
                'O': 5
            }).scaleUp(*INDICATOR_SCALE),
            BitmapFrame(5, 6, [
                '     ',
                '     ',
                '     ',
                '     ',
                '     ',
                '     '
            ], {
                ' ': -1,
                'O': 8
            }).scaleUp(*INDICATOR_SCALE)
        ]
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

