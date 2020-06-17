from sheet.gen.abs_output import AbsNote
from game.constants import Constants
from game.config import *
from game.frames import *
from game.playthrough.base_note import *
import game.playthrough.criteria_manager as cm
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
        # self.direction = Constants.PlayThrough.DIRECTIONS[note.side]
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
        progress = (total_time - self.prop["offset"]) / self.prop["pass_time"]
        try:
            self.pos = cm.get_pos_in_progress(self, progress)
        except TypeError as e:
            print(e)
            print("Move failed because of the error above...")
            
    def __repr__(self):
        return f"Note {self.note}"
    def update(self, total_time: float) -> int:
        if self.is_time(total_time) and not self.finished:
            self.in_scene = True
            self.finished = False
        if (not self.finished) and self.in_scene:
            self.move(total_time)
            result = Constants.PlayThrough.IndicateWithTime(
                self.prop["side"], self.prop["offset"],
                self.prop["pass_time"], total_time
            )
            if result != Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND:
                if Config.TOUCHED[self.prop["side"]] or result == Constants.PlayThrough.NoteIndicator.MISS:
                    
                    self.finished = True
                    self.in_scene = False
                    self.result   = result
                    
                    Config.TOUCHED[self.prop["side"]] = False
                    return self.result
        return Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND
    def draw(self):
        if (not self.finished) and self.in_scene:
            frame = Frames.PlayThrough.DIRECTIONS[self.prop["side"]]
            frame.draw(self.pos[0] - frame.width / 2, self.pos[1] - frame.height / 2)
