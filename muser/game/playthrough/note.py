from sheet.gen.abs_output import AbsNote
from game.constants import Constants
from game.config import *
from game.frames import *
from game.playthrough.base_note import *
import math
import pyxel
import copy
import json
import util
class PositionedNote(BaseNote):

    def __init__(self, note: AbsNote):
        self.note: AbsNote = note
        self.prop = self.note.prop
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
        if (not self.in_scene) and (not self.finished) and (total_time >= self.prop["offset"]):
            return True
        else:
            return False
    def move(self, total_time: float):
        # pixels = Constants.PlayThrough.DISTANCES()[self.prop["side"]] * (total_time - self.prop["offset"]) / self.prop["pass_time"]
        # # pixels = Constants.PlayThrough.DISTANCES()[self.prop["side"]] * (2000) / self.prop["pass_time"]
        # self.pos[0] = self.initial_pos[0] + self.direction[0] * pixels
        # self.pos[1] = self.initial_pos[1] + self.direction[1] * pixels
        # # print(f"Move {str(self.note.__repr__())} {pixels} pixels to {self.pos} from {self.initial_pos}")
        center = Constants.Cast.center(0, 0)
        
        init_to_center_vec = (center[0] - self.initial_pos[0], center[0] - self.initial_pos[1])
        percent_passed = (total_time - self.prop["offset"]) / self.prop["pass_time"]
        self.pos[0] = self.initial_pos[0] + init_to_center_vec[0] * percent_passed
        self.pos[1] = self.initial_pos[1] + init_to_center_vec[1] * percent_passed
    def __repr__(self):
        return f"Note {self.note}"
    def update(self, total_time: float) -> int:
        if self.is_time(total_time) and not self.finished:
            print(f"Note in scene at {total_time}: {str(self.note.__repr__())}")
            self.in_scene = True
            self.finished = False
        if (not self.finished) and self.in_scene:
            self.move(total_time)
            result = Constants.PlayThrough.IndicatorRange(
                self.prop["side"], self.pos)
            # if Config.TOUCHED[self.prop["side]:
                # print(
                #     f"This note is in bound and is touched at {self.pos}, distance to center: {Constants.PlayThrough.DistanceToCenter(self.pos)}: {self.note}, result: {Constants.PlayThrough.NoteIndicator.INDICATOR_NAME[result]}")
            if result != Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND:
                # print(f"{self.note} {Config.TOUCHED}, {Constants.PlayThrough.NoteIndicator.INDICATOR_NAME[result]}")
                if Config.TOUCHED[self.prop["side"]] or result == Constants.PlayThrough.NoteIndicator.MISS:
                    self.finished = True
                    self.in_scene = False
                    self.result = result
                    Config.TOUCHED[self.prop["side"]] = False
                    print(f"Note {str(self.note.__repr__())} finished at {self.pos}, {total_time}, {Constants.PlayThrough.NoteIndicator.INDICATOR_NAME[self.result]}")
                    return self.result
        return Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND
    def draw(self):
        if (not self.finished) and self.in_scene:
            frame = Frames.PlayThrough.DIRECTIONS[self.prop["side"]]
            frame.draw(self.pos[0] - frame.width / 2, self.pos[1] - frame.height / 2)
        # elif self.finished and not self.animation_finished:
        #     Frames.PlayThrough.ARROW_FADE[self.prop["side].draw(self.pos[0] - 4, self.pos[1] - 4)
        #     self.animation_finished = True
