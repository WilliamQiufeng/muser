from game.frames import *
from game.constants import *
from game.widgets import *
from game.config import *
from game.playthrough.note_manager import *
from sheet.reader.sheet_reader import *
from game.sounds import *
import util as util
import pyxel
import pygame
import io, sys, os


pygame.mixer.init()

class Cast:
    def update(self):
        raise NotImplementedError
    def draw(self):
        raise NotImplementedError
    def is_finished(self):
        raise NotImplementedError
    def next_cast(self):
        raise NotImplementedError
    def clear_screen(self):
        pyxel.cls(0)
class Casts:
    class Intro(Cast):
        def __init__(self):
            self.frame = 0
            self.finished = False
        def update(self):
            if pyxel.btn(pyxel.KEY_ENTER):
                self.finished = True # Skip the starting screen
                return None
            self.frame += 0 if self.finished else 1
            if len(Frames.Intro.WHOLE) <= self.frame:
                self.finished = True
                self.frame = len(Frames.Intro.WHOLE) - 1
        def draw(self):
            cur_frame = Frames.Intro.WHOLE[self.frame]
            pos = Constants.Cast.center(cur_frame.width, cur_frame.height)
            cur_frame.draw(*pos)
        def is_finished(self):
            return self.finished
        def next_cast(self):
            return Casts.LevelSelection()

    class LevelSelection(Cast):
        BUTTONS = [
            Button(16, Constants.Cast.center(16, 16)[1], pyxel.KEY_LEFT,Frames.LevelSelection.LEFT_PRESSED, Frames.LevelSelection.LEFT_UNPRESSED, lambda: Casts.LevelSelection.increase(Config.CAST, -1)),
            Button(Constants.Cast.WIDTH - 32, Constants.Cast.center(16, 16)[1], pyxel.KEY_RIGHT,Frames.LevelSelection.RIGHT_PRESSED, Frames.LevelSelection.RIGHT_UNPRESSED, lambda: Casts.LevelSelection.increase(Config.CAST, 1)),
            Button(Constants.Cast.center(16, 16)[0], Constants.Cast.HEIGHT - 32, pyxel.KEY_SPACE, Frames.LevelSelection.PLAY_PRESSED, Frames.LevelSelection.PLAY_UNPRESSED, lambda: Casts.LevelSelection.select(Config.CAST)),
            KeyListener(pyxel.KEY_UP, on_click=lambda: Casts.LevelSelection.increaseLevel(Config.CAST, 1)),
            KeyListener(pyxel.KEY_DOWN, on_click=lambda: Casts.LevelSelection.increaseLevel(
                Config.CAST, -1))
        ]
        @staticmethod
        def increase(obj, inc):
            obj.selection += inc
            if obj.selection >= len(obj.sheets):
                obj.selection = 0
            if obj.selection < 0:
                obj.selection = len(obj.sheets) - 1
            obj.update_meta()

        @staticmethod
        def increaseLevel(obj, inc):
            obj.level_selection += inc
            if obj.level_selection >= len(obj.sheet):
                obj.level_selection = 0
            if obj.level_selection < 0:
                obj.level_selection = len(obj.sheet) - 1
        @staticmethod
        def select(obj):
            obj.finished = True
        def __init__(self):
            self.selection = 0
            self.level_selection = 0
            self.finished = False
            self.sheets = []
            for path in Config.SHEET_PATHS:
                for file in os.listdir(path):
                    if file.endswith(".sheet"):
                        self.sheets.append(path + file)
            print(self.sheets)
            self.update_meta()
        def update_meta(self):
            self.level_selection = 0
            self.sheet = SheetReader.from_sheets(self.sheets[self.selection])
            self.music_source = self.sheet[self.level_selection].data["music"]
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music_source)
            pygame.mixer.music.play()
        def update(self):
            for btn in Casts.LevelSelection.BUTTONS:
                btn.update()
        def draw(self):
            for btn in Casts.LevelSelection.BUTTONS:
                if "draw" in dir(btn):
                    btn.draw()
            positions = [
                util.grid(Constants.Cast.WIDTH, Constants.Cast.HEIGHT, 3, 7, 1, x + 1) for x in range(5)]
            level = self.sheet[self.level_selection]
            pyxel.text(*positions[0], f'{level.data["name"]}', 12)
            pyxel.text(*positions[1], f'Sheet Author: {level.data["author"]}', 11)
            pyxel.text(*positions[2], f'Music Author: {level.data["music_author"]}', 10)
            pyxel.text(*positions[3], f'Version:      {level.data["version"]}', 9)
            pyxel.text(*positions[4], f'Level:        {level.data["level"]}', 8)
        def is_finished(self):
            return self.finished
        def next_cast(self):
            return Casts.PlayThrough(self.sheet[self.level_selection], self.music_source)
    class PlayThrough(Cast):
        UPDATES = [
            KeyListener(
                pyxel.KEY_S, on_touch=lambda: Casts.PlayThrough.touch(0)),
            KeyListener(
                pyxel.KEY_W, on_touch=lambda: Casts.PlayThrough.touch(1)),
            KeyListener(
                pyxel.KEY_D, on_touch=lambda: Casts.PlayThrough.touch(2)),
            KeyListener(
                pyxel.KEY_A, on_touch=lambda: Casts.PlayThrough.touch(3)),
            KeyListener(
                pyxel.KEY_K, on_touch=lambda: Casts.PlayThrough.touch(0)),
            KeyListener(
                pyxel.KEY_I, on_touch=lambda: Casts.PlayThrough.touch(1)),
            KeyListener(
                pyxel.KEY_L, on_touch=lambda: Casts.PlayThrough.touch(2)),
            KeyListener(
                pyxel.KEY_J, on_touch=lambda: Casts.PlayThrough.touch(3))
        ]
        @staticmethod
        def touch(side: int):
            Config.TOUCHED[side] = True
            #print(Config.TOUCHED)
        def __init__(self, sheet: SheetReader, music_source):
            self.sheet: SheetReader = sheet
            self.music_source = music_source
            self.finished: bool = False
            self.quit: bool = False
            self.note_manager: NoteManager = NoteManager(self.sheet, Constants.PlayThrough.DISTANCES(), self.music_source)
            self.note_manager.prepare()
            self.note_manager.start()

        @util.timeit(without=(-1, 30))
        def update(self):
            Config.TOUCHED = [False for _ in range(4)]
            for upd in Casts.PlayThrough.UPDATES:
                upd.update()
            # print(f"last: {Config.TOUCHED}")
            self.note_manager.update()
            # print(f"cur: {Config.TOUCHED}")
            self.finished = self.note_manager.finished
            if pyxel.btnp(pyxel.KEY_P):
                self.note_manager.pause()
            self.quit = pyxel.btn(pyxel.KEY_Q)
            if self.quit:
                print("Quit playthrough.")
                EffectController.clear_effects()
                print("Effects cleared")

        @util.timeit(without=(-1, 30))
        def draw(self):
            self.note_manager.draw()
        def is_finished(self):
            return self.finished or self.quit
        def next_cast(self):
            return Casts.Result(self) if self.finished else Casts.LevelSelection()
    class Result(Cast):
        UPDATES = [
            KeyListener(pyxel.KEY_ENTER, on_click=lambda: Casts.Result.finish(Config.CAST))
        ]
        @staticmethod
        def finish(obj):
            if not obj.animating:
                obj.prefinished = True
                obj.prefinish_frame = pyxel.frame_count
                obj.animating = True
                pygame.mixer.music.stop()
        def __init__(self, play_through):
            self.play_through = play_through
            self.finished = False
            self.prefinished = False
            self.animating = False
            # self.animation_bitmap = [(x, y) for x in range(Constants.Cast.WIDTH) for y in range(Constants.Cast.HEIGHT)]
            total_pixels = Constants.Cast.WIDTH * Constants.Cast.HEIGHT
            self.animation_bitmap = random.sample(range(0, total_pixels), total_pixels)
            self.score_percentage = self.play_through.note_manager.score / Constants.PlayThrough.Score.TOTAL_SCORE * 100
            self.grade_frame = Constants.Result.Grade.getGradeFrame(self.score_percentage)
            self.count = NoteManager.count(self.play_through.note_manager)
            self.tp = self.count.get_tp()
            self.score = int(self.play_through.note_manager.score)
            if self.score_percentage >= Constants.Result.Grade.A:
                Sounds.Grade.A.play()
            else:
                Sounds.Grade.C.play()
            
        def update(self):
            for upd in Casts.Result.UPDATES:
                upd.update()
        def draw(self):
            if not self.animating:
                pyxel.cls(2 if self.score_percentage >= Constants.Result.Grade.A else 3)
                counter_positions = [util.grid(
                    Constants.Cast.WIDTH, Constants.Cast.HEIGHT, 5, 16, 1 + (x % 2) * 2, 12 + (0 if x < 2 else 1)) for x in range(4)]
                tp_pos = util.grid(Constants.Cast.WIDTH, Constants.Cast.HEIGHT, 5, 16, 2, 12.5)
                score_pos = util.grid(Constants.Cast.WIDTH, Constants.Cast.HEIGHT, 5, 16, 2, 11)
                count_prop = self.count.get_prop()
                pyxel.text(*tp_pos, "TP: {0:.2f}%".format(self.tp), 13)
                pyxel.text(*score_pos, f"Score: {self.score}", 14)
                for x in range(4):
                    key = list(count_prop.keys())[x]
                    pyxel.text(*counter_positions[x], f"{key}: {count_prop[key]}", 12 - x)
                self.grade_frame.draw(*Constants.Cast.center(self.grade_frame.width, self.grade_frame.height))
            if self.animating and not self.finished:
                for i in range(Constants.Result.ANIMATION_SPEED):
                    if len(self.animation_bitmap) == 0:
                        self.animating = False
                        self.finished = True
                        break
                    rand = self.animation_bitmap.pop()
                    x = rand % Constants.Cast.WIDTH
                    pos = [(rand - x) / Constants.Cast.WIDTH, x]
                    pyxel.pix(*pos, 8)
        def is_finished(self):
            return self.finished
        def next_cast(self):
            return Casts.LevelSelection()
        def clear_screen(self):
            if not self.animating:
                super().clear_screen()

Config.CAST = Casts.Intro()
