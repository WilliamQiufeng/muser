from sheet.gen.abs_output import AbsNote
from game.constants import Constants
from game.config import *
from game.frames import *
from game.playthrough.base_note import *
import math
import pyxel
import copy
class PositionedNote(BaseNote):

    def __init__(self, note: AbsNote):
        self.note: AbsNote = note
        self.initial_pos = Constants.PlayThrough.InitialPos(note.side)
        self.pos = copy.copy(self.initial_pos)
        self.direction = Constants.PlayThrough.DIRECTIONS[note.side]
        self.in_scene: bool = False
        self.finished: bool = False
        self.animation_finished: bool = False
        self.result = Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND
    @property
    def len_to_center(self, center: tuple):
        return math.sqrt((self.initial_pos[0] - center[0])** 2 + (self.initial_pos[1] - center[1])** 2)
    def is_time(self, total_time: int):
        if (not self.in_scene) and (not self.finished) and (total_time >= self.note.offset):
            return True
        else:
            return False
    def move(self, total_time: float):
        pixels = (Constants.PlayThrough.DISTANCES()[self.note.side] * (total_time - self.note.offset)) / self.note.pass_time
        self.pos[0] = self.initial_pos[0] + self.direction[0] * pixels
        self.pos[1] = self.initial_pos[1] + self.direction[1] * pixels
        #print(f"Move {self.note} {pixels} pixels to {self.pos} from {self.initial_pos}")
    def __repr__(self):
        return f"Note {self.note}"
    def update(self, total_time: float) -> int:
        if self.is_time(total_time) and not self.finished:
            print(f"Note in scene at {total_time}: {self.note}")
            self.in_scene = True
            self.finished = False
        if (not self.finished) and self.in_scene:
            self.move(total_time)
            result = Constants.PlayThrough.IndicatorRange(
                self.note.side, self.pos)
            # if Config.TOUCHED[self.note.side]:
                # print(
                #     f"This note is in bound and is touched at {self.pos}, distance to center: {Constants.PlayThrough.DistanceToCenter(self.pos)}: {self.note}, result: {Constants.PlayThrough.NoteIndicator.INDICATOR_NAME[result]}")
            if result != Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND:
                # print(f"{self.note} {Config.TOUCHED}, {Constants.PlayThrough.NoteIndicator.INDICATOR_NAME[result]}")
                if Config.TOUCHED[self.note.side] or result == Constants.PlayThrough.NoteIndicator.MISS:
                    self.finished = True
                    self.in_scene = False
                    self.result = result
                    Config.TOUCHED[self.note.side] = False
                    print(f"Note {self.note} finished at {self.pos}, {total_time}, {Constants.PlayThrough.NoteIndicator.INDICATOR_NAME[self.result]}")
                    return self.result
        return Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND
    def draw(self):
        if (not self.finished) and self.in_scene:
            Frames.PlayThrough.DIRECTIONS[self.note.side].draw(self.pos[0] - 3, self.pos[1] - 3)
        # elif self.finished and not self.animation_finished:
        #     Frames.PlayThrough.ARROW_FADE[self.note.side].draw(self.pos[0] - 4, self.pos[1] - 4)
        #     self.animation_finished = True
