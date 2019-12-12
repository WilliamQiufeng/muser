from game.frames import *
import math
from game.config import *
class Constants:
    class Cast:
        WIDTH = 256
        HEIGHT = 256
        INTRO = 0
        MUSIC_SELECTION = 1
        PLAY = 2
        CENTER_X = WIDTH / 2
        CENTER_Y = HEIGHT / 2
        @staticmethod
        def center(w, h) -> tuple:
            return (Constants.Cast.WIDTH / 2 - w / 2, Constants.Cast.HEIGHT / 2 - h / 2)
    class PlayThrough:
        UP = (0, -1)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        RIGHT = (1, 0)
        DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
        INITIALS = [(0.5, 1), (0.5, 0), (1, 0.5), (0, 0.5)]
        OFFSETS = [(0, -16), (0, 0), (-16, 0), (0, 0)]
        
        class Score:
            TOTAL_SCORE = 100000

        class NoteIndicator:
            PERFECT = 4
            GREAT = 10
            BAD = 16
            MISS = 17
            NOT_IN_BOUND = 18
            INDICATOR_NAME = {4: "PERFECT", 10: "GREAT", 16: "BAD", 17: "MISS", 18: "Not In Bound"}
            @staticmethod
            def INDICATORS():
                return [Constants.PlayThrough.NoteIndicator.MISS, Constants.PlayThrough.NoteIndicator.BAD, Constants.PlayThrough.NoteIndicator.GREAT, Constants.PlayThrough.NoteIndicator.PERFECT]
            @staticmethod
            def getFrame(indicator: int) -> Frame:
                order = [Constants.PlayThrough.NoteIndicator.PERFECT, Constants.PlayThrough.NoteIndicator.GREAT,
                        Constants.PlayThrough.NoteIndicator.BAD, Constants.PlayThrough.NoteIndicator.MISS,
                        Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND]
                return Frames.PlayThrough.INDICATOR_RES[order.index(indicator)]

        @staticmethod
        def DISTANCES() -> list:
            return [Constants.Cast.HEIGHT / 2] * 2 + [Constants.Cast.WIDTH / 2] * 2

        @staticmethod
        def DistanceToCenter(pos: list) -> int:
            center: tuple = Constants.PlayThrough.CENTER()
            return math.sqrt((pos[0] - center[0]) **
                      2 + (pos[1] - center[1]) ** 2) 
        @staticmethod
        def CENTER() -> tuple:
            return Constants.Cast.center(0, 0)
        @staticmethod
        def InitialPos(side: int) -> list:
            initials: tuple = Constants.PlayThrough.INITIALS[side]
            pos: list = (
                initials[0] * Constants.Cast.WIDTH, initials[1] * Constants.Cast.HEIGHT)
            res: list = [
                pos[0],# + Constants.PlayThrough.OFFSETS[0],
                pos[1],# + Constants.PlayThrough.OFFSETS[1]
            ]
            return res

        @staticmethod
        def IndicatorGet(side: int, indicator: int) -> tuple:
            center: list = list(Constants.PlayThrough.CENTER())
            axis: tuple = (center[0] + Constants.PlayThrough.DIRECTIONS[side][0] * indicator,  # + Constants.PlayThrough.OFFSETS[side][0]
                           center[1] + Constants.PlayThrough.DIRECTIONS[side][1] * indicator)  # + Constants.PlayThrough.OFFSETS[side][1]
            return axis
        @staticmethod
        def IndicatorMiss(side: int) -> tuple:
            return Constants.PlayThrough.IndicatorGet(side, Constants.PlayThrough.NoteIndicator.MISS)
        @staticmethod
        def IndicatorRange(side: int, pos: list) -> int:
            touched = Config.TOUCHED[side]
            if touched:
                dist = Constants.PlayThrough.DistanceToCenter(pos)
                if dist <= Constants.PlayThrough.NoteIndicator.PERFECT:
                    return Constants.PlayThrough.NoteIndicator.PERFECT
                elif dist <= Constants.PlayThrough.NoteIndicator.GREAT:
                    return Constants.PlayThrough.NoteIndicator.GREAT
                elif dist <= Constants.PlayThrough.NoteIndicator.BAD:
                    return Constants.PlayThrough.NoteIndicator.BAD
            miss_line = Constants.PlayThrough.IndicatorMiss(side)
            direction = Constants.PlayThrough.DIRECTIONS[side]
            if (pos[0] != Constants.PlayThrough.InitialPos(side)[0] and pos[0] * direction[0] > miss_line[0] * direction[0]) or (
                pos[1] != Constants.PlayThrough.InitialPos(side)[1] and pos[1] * direction[1] > miss_line[1] * direction[1]):
                return Constants.PlayThrough.NoteIndicator.MISS
            else:
                return Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND
            
    class Result:
        class Grade:
            FAIL = 0
            D = 60
            C = 70
            B = 80
            A = 90
            S = 95
            @staticmethod
            def getGradeFrame(score: int) -> Frame:
                res = Frames.Result.F
                if score >= Constants.Result.Grade.FAIL:
                    res = Frames.Result.F
                if score >= Constants.Result.Grade.D:
                    res = Frames.Result.D
                if score >= Constants.Result.Grade.C:
                    res = Frames.Result.C
                if score >= Constants.Result.Grade.B:
                    res = Frames.Result.B
                if score >= Constants.Result.Grade.A:
                    res = Frames.Result.A
                if score >= Constants.Result.Grade.S:
                    res = Frames.Result.S
                return res
