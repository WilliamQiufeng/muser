import game_config
from game.frame import Frame, BitmapFrame


class Frames:
    class Init:
        DIRECTORY = Frame(0, 216, 16, 16)
        FILE = Frame(16, 216, 16, 16)
        BACK = Frame(32, 216, 16, 16)
        ENTER = Frame(48, 216, 16, 16)

    class Intro:
        EMPTY = [Frame(80, 136, 79, 16)]
        TITLE_PRE = EMPTY * 20
        TITLE_FADEIN = [Frame(0, 136 + 16 * x, 79, 16) for x in range(0, 5)
                        for _ in range(int(game_config.GLOB_CONFIG.config["fps"] / 15))]
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
        UP_UNPRESSED, DOWN_UNPRESSED, UP_PRESSED, DOWN_PRESSED = (
            Frame(80 + 16 * x, 24, 16, 16) for x in range(4))
        PLAY_UNPRESSED = Frame(0, 64, 16, 16)
        PLAY_PRESSED = Frame(16, 64, 16, 16)

    class PlayThrough:
        # DIRECTIONS = [Frame(1 + x * 8, 5, 6, 6) for x in range(4)]
        # DIRECTIONS = [ArrowFrame(x) for x in range(12)]
        DIRECTIONS = [
            BitmapFrame.from_pyxel((x * 8 + 1, y * 8 + 1), (6, 6))
            for y in range(2)
            for x in range(6)
        ]
        ARROW_FADE = [Frame(56 + 8 * x, 4, 8, 8) for x in range(4)]
        # INDICATOR_CIRCLE = Frame(32, 48, 32, 32)
        INDICATOR_CIRCLE = BitmapFrame.from_pyxel((32, 48), (32, 32))
        # INDICATOR_CIRCLE = BitmapFrame(32, 32, [
        #     "            H      H            ",
        #     "            H      H            ",
        #     "                                ",
        #     "                                ",
        #     "            H      H            ",
        #     "            H      H            ",
        #     "            H      H            ",
        #     "       HHHHHH      HHHHHH       ",
        #     "       HHHHH        HHHHH       ",
        #     "       HH              HH       ",
        #     "       HH              HH       ",
        #     "       HH              HH       ",
        #     "HH  HHHH                HHHH  HH",
        #     "                                ",
        #     "                                ",
        #     "                                ",
        #     "                                ",
        #     "                                ",
        #     "                                ",
        #     "HH  HHHH                HHHH  HH",
        #     "       HH              HH       ",
        #     "       HH              HH       ",
        #     "       HH              HH       ",
        #     "       HHHHH        HHHHH       ",
        #     "       HHHHHH      HHHHHH       ",
        #     "            H      H            ",
        #     "            H      H            ",
        #     "            H      H            ",
        #     "                                ",
        #     "                                ",
        #     "            H      H            ",
        #     "            H      H            "
        # ], {
        #     " ": -1,
        #     "H": 8,
        # })
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
