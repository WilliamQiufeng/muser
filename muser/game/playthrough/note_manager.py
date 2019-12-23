import copy
import time
import pygame
from sheet.reader.sheet_reader import *
from game.playthrough.manager_actions import *
from game.constants import *
from game.playthrough.effect.effect_controller import *
import util as util

pygame.mixer.init()


class Counter:
    def __init__(self):
        self.misses = 0
        self.bads = 0
        self.greats = 0
        self.perfects = 0
    def get_prop(self):
        return {
            "Perfects": self.perfects,
            "Greats": self.greats,
            "Bads": self.bads,
            "Misses": self.misses
        }
    def get_total_notes(self):
        return self.misses + self.bads + self.greats + self.perfects
    def get_tp(self):
        total_notes = self.get_total_notes()
        weight_count = self.misses * 0 + self.bads * 1 + self.greats * 2 + self.perfects * 3
        avg_weight  = weight_count / total_notes
        tp = avg_weight / 0.03
        return tp
class NoteManager:
    @staticmethod
    def count(manager):
        counter = Counter()
        for note in manager.notes:
            if not isinstance(note, PositionedNote):
                continue
            if note.result == Constants.PlayThrough.NoteIndicator.PERFECT:
                counter.perfects += 1
            elif note.result == Constants.PlayThrough.NoteIndicator.GREAT:
                counter.greats += 1
            elif note.result == Constants.PlayThrough.NoteIndicator.BAD:
                counter.bads += 1
            elif note.result == Constants.PlayThrough.NoteIndicator.MISS:
                counter.misses += 1
        return counter
    def __init__(self, sheet: SheetReader, side_distances : list, music_source : str):
        self.meta: dict = sheet.metadata
        self.notes: list = [ManagerActions.from_note(x) for x in sheet.notes]
        print("\n".join([str(x) for x in self.notes]))
        self.side_distances: list = side_distances
        self.music_source: str = music_source
        self.music_started: bool = False
        self.started: bool = False
        self.initiate: bool = True
        self.finished: bool = False
        self.score: int = 0
        self.perfect_note_score = Constants.PlayThrough.Score.TOTAL_SCORE / (len(self.notes) * Constants.PlayThrough.NoteIndicator.INDICATORS().index(Constants.PlayThrough.NoteIndicator.PERFECT))
    def prepare(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music_source)
    def start(self):
        self.initiate = True
        
    def update_time(self) -> float:
        cur_time = time.time()
        if self.music_started:
            self.total_time = (
                self.meta["offset"] + pygame.mixer.music.get_pos()) / 1000
            cur_time = self.total_time
            #print(
            #    f"Total Time: {self.total_time}, Cur Time: {cur_time}, Interval: {interval}, Last Time: {self.last_time}")
        else:
            self.total_time = cur_time - self.start_time
            #print(
            #    f"Total Time: {self.total_time}, Cur Time: {cur_time}, Interval: {interval}, Last Time: {self.last_time}")
        if (not self.music_started) and self.total_time * 1000 >= self.meta["offset"]:
            # pygame.mixer.music.set_pos(self.total_time * 1000 - self.meta["offset"])
            print(self.total_time)
            pygame.mixer.music.play()
            self.music_started = True
            cur_time = (self.meta["offset"] +
                        pygame.mixer.music.get_pos()) / 1000
            self.total_time = self.total_time
            print(
                f"Total Time: {self.total_time}, Cur Time: {cur_time}, Start Time: {self.start_time}")
        return cur_time
    def update(self):
        if self.initiate:
            self.start_time = time.time()
            self.total_time: float = 0
            self.initiate = False
            self.started = True
            self.finished = False
            self.last_indicator = Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND
        cur_time: float = self.update_time()
        EffectController.update(total_time=self.total_time * 1000)
        if self.music_started and not pygame.mixer.music.get_busy():
            self.finished = True
            return None
        res = Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND
        for note in self.notes:
            res_indicate = note.update(self.total_time * 1000)
            if not isinstance(note, PositionedNote):
                continue
            if res_indicate != Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND:
                res = res_indicate
                if res_indicate != Constants.PlayThrough.NoteIndicator.MISS:
                    self.score += self.perfect_note_score * Constants.PlayThrough.NoteIndicator.INDICATORS().index(res_indicate)
        if res != Constants.PlayThrough.NoteIndicator.NOT_IN_BOUND:
            self.last_indicator = res
    
    def draw(self):
        EffectController.draw(total_time=self.total_time)
        pyxel.text(*util.grid(
            Constants.Cast.WIDTH, Constants.Cast.HEIGHT,
            16, 16,
            12, 1
        ), f"Score: {int(self.score)}", 12)
        Frames.PlayThrough.INDICATOR_CIRCLE.draw(*Constants.Cast.center(
            Frames.PlayThrough.INDICATOR_CIRCLE.width, Frames.PlayThrough.INDICATOR_CIRCLE.height))
        # indicator_res = Constants.PlayThrough.NoteIndicator.getFrame(
        #     self.last_indicator)
        # indicator_res.draw(
        #     *Constants.Cast.center(indicator_res.width, indicator_res.height))
        Constants.PlayThrough.NoteIndicator.getFrame(self.last_indicator).draw(*util.grid(
            Constants.Cast.WIDTH, Constants.Cast.HEIGHT,
            16, 16,
            1, 1
        ))
        for note in self.notes:
            note.draw()
