from game.frames import Frames
from game.constants import Constants
from game.widgets import KeyListener, Button
from game.config import Config
from game.playthrough.note_manager import NoteManager
from sheet.reader.sheet_reader import SheetReader
from game.playthrough.effect.effect_controller import EffectController
from game.sounds import Sounds
import game_config
import util as util
import pyxel
from pyglet import media
import os
import random
import logger

# flake8: noqa: E241


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
    # class Init(Cast):
    #     def __init__(self):
    #         self.finished = (game_config.GLOB_CONFIG.config_path is not None) and os.path.isfile(game_config.GLOB_CONFIG.config_path)
    #         self.path = os.path.abspath(".")
    #         self.file_chosen = None
    #         self.current_dir_files = self.list_files()

    #     def goto_previous_dir(self):
    #         self.path = os.path.dirname(self.path)

    #     def goto_dir(self, name):
    #         self.path = os.path.join(self.path, name)

    #     def choose_file(self, name):
    #         self.file_chosen = os.path.join(self.path, name)

    #     def list_files(self):
    #         return os.listdir(self.path)

    #     def update(self):
    #         if pyxel.btnp(pyxel.KEY_ENTER):
    #             if os.path.isdir(self.file_chosen):
    #                 self.goto_dir(self.file_chosen)
    #             elif os.path.isfile(self.file_chosen):
    #                 pass
    #     def draw(self):
    #         pass
    #     def is_finished(self):
    #         return self.finished
    #     def next_cast(self):
    #         return Casts.Intro()
    class Intro(Cast):
        def __init__(self):
            self.frame = 0
            self.finished = False

        def update(self):
            if pyxel.btn(pyxel.KEY_ENTER):
                self.finished = True  # Skip the starting screen
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
            Button(
                16, Constants.Cast.center(16, 16)[1],
                pyxel.KEY_LEFT, Frames.LevelSelection.LEFT_PRESSED,
                Frames.LevelSelection.LEFT_UNPRESSED,
                lambda: Casts.LevelSelection.increase(
                    Config.CAST, -1)),
            Button(
                Constants.Cast.WIDTH - 32, Constants.Cast.center(
                    16, 16)[1],
                pyxel.KEY_RIGHT, Frames.LevelSelection.RIGHT_PRESSED,
                Frames.LevelSelection.RIGHT_UNPRESSED,
                lambda: Casts.LevelSelection.increase(
                    Config.CAST, 1)),
            Button(
                Constants.Cast.center(16, 16)[0],
                Constants.Cast.HEIGHT - 32, pyxel.KEY_SPACE, Frames.
                LevelSelection.PLAY_PRESSED, Frames.LevelSelection.
                PLAY_UNPRESSED, lambda: Casts.LevelSelection.select(
                    Config.CAST)),
            KeyListener(
                pyxel.KEY_UP,
                on_click=lambda: Casts.LevelSelection.increaseLevel(
                    Config.CAST, 1)),
            KeyListener(
                pyxel.KEY_DOWN,
                on_click=lambda: Casts.LevelSelection.increaseLevel(
                    Config.CAST, -1)),
            KeyListener(
                pyxel.KEY_S,
                on_click=lambda: Casts.LevelSelection.settings(
                    Config.CAST)),
            KeyListener(
                pyxel.KEY_A,
                on_click=lambda: Casts.LevelSelection.toggle_auto_mod()
            )]
        
        @staticmethod
        def toggle_auto_mod():
            Config.MOD_AUTO = not Config.MOD_AUTO

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
            Config.release_player()
            obj.finished = True

        @staticmethod
        def settings(obj):
            Config.release_player()
            # pygame.mixer.music.stop()
            obj.finished = True
            obj.goto_settings = True

        def __init__(self):
            self.selection = 0
            self.level_selection = 0
            self.finished = False
            self.goto_settings = False
            self.sheets = []
            for path in Config.SHEET_PATHS:
                for file in os.listdir(path):
                    if file.endswith(".sheet"):
                        self.sheets.append(os.path.join(path, file))
            # logger.print(self.sheets)
            self.update_meta()

        def update_meta(self):
            self.level_selection = 0
            self.sheet = SheetReader.from_sheets(self.sheets[self.selection])
            self.music_source = self.sheet[self.level_selection].data["music"]
            self.music: media.Source = media.load(self.music_source)

            Config.release_player()
            Config.PLAYER = self.music.play()

        def update(self):
            for btn in Casts.LevelSelection.BUTTONS:
                btn.update()

        def draw(self):
            pyxel.text(0, 0,  "Hardness        [Up/Down]", 12)
            pyxel.text(0, 6,  "Level Selection [Left/Right]", 12)
            pyxel.text(0, 12, "Play            [Space]", 12)
            pyxel.text(0, 18, "Settings        [S]", 12)
            pyxel.text(0, 24, "Quit            [Q]", 12)
            pyxel.text(0, 30, f"Auto: {str(Config.MOD_AUTO).ljust(5)}     [A]", 12)
            for btn in Casts.LevelSelection.BUTTONS:
                if "draw" in dir(btn):
                    btn.draw()
            positions = [
                util.grid(
                    Constants.Cast.WIDTH, Constants.Cast.HEIGHT, 3, 7, 1, x + 1)
                for x in range(5)]
            level = self.sheet[self.level_selection]
            pyxel.text(*positions[0], f'{level.data["name"]}', 12)
            pyxel.text(
                *positions[1],
                f'Sheet Author: {level.data["author"]}', 11)
            pyxel.text(
                *positions[2],
                f'Music Author: {level.data["music_author"]}', 10)
            pyxel.text(
                *positions[3],
                f'Version:      {level.data["version"]}', 9)
            pyxel.text(
                *positions[4],
                f'Level:        {level.data["level"]}', 8)

        def is_finished(self):
            return self.finished

        def next_cast(self):

            return Casts.Settings() if self.goto_settings else Casts.PlayThrough(self.sheet[self.level_selection], self.music_source)

    class PlayThrough(Cast):
        UPDATES = []
        controls = game_config.GLOB_CONFIG.controls
        keys = list(controls.keys())
        for n in range(len(keys) - 2):
            lamb = lambda n=n: Casts.PlayThrough.touch(n)
            UPDATES.append(KeyListener(controls[keys[n]], on_touch=lamb))


        @staticmethod
        def touch(side: int):
            Config.TOUCHED[side] = True
            # logger.print(Config.TOUCHED)

        def __init__(self, sheet: SheetReader, music_source):
            self.sheet: SheetReader = sheet
            self.music_source = music_source
            self.finished: bool = False
            self.quit: bool = False
            self.note_manager: NoteManager = NoteManager(
                self.sheet, Constants.PlayThrough.DISTANCES(), self.music_source)
            self.note_manager.prepare()
            self.note_manager.start()

        @util.timeit(without=(-1, 30))
        def update(self):
            # If Config.MOD_AUTO, all touched is set to true
            Config.TOUCHED = [Config.MOD_AUTO] * 16
            for upd in Casts.PlayThrough.UPDATES:
                upd.update()
            # logger.print(f"last: {Config.TOUCHED}")
            self.note_manager.update()
            # logger.print(f"cur: {Config.TOUCHED}")
            self.finished = self.note_manager.finished
            if pyxel.btnp(pyxel.KEY_P):
                self.note_manager.pause()
            self.quit = pyxel.btn(pyxel.KEY_Q)
            if self.quit:
                logger.print("Quit playthrough.")
                EffectController.clear_effects()
                # logger.print("Effects cleared")

        @util.timeit(without=(-1, 30))
        def draw(self):
            self.note_manager.draw()
            if Config.MOD_AUTO:
                pyxel.text(232, 250, "AUTO", 12)

        def is_finished(self):
            return self.finished or self.quit

        def next_cast(self):
            return Casts.Result(self) if self.finished else Casts.LevelSelection()

    class Result(Cast):
        UPDATES = [
            KeyListener(
                pyxel.KEY_ENTER, on_click=lambda: Casts.Result.finish(
                    Config.CAST))]

        @staticmethod
        def finish(obj):
            if not obj.animating:
                obj.prefinished = True
                obj.prefinish_frame = pyxel.frame_count
                obj.animating = True
                # pygame.mixer.music.stop()

        def __init__(self, play_through):
            self.play_through = play_through
            self.finished = False
            self.prefinished = False
            self.animating = False
            total_pixels = Constants.Cast.WIDTH * Constants.Cast.HEIGHT
            self.animation_bitmap = random.sample(
                range(total_pixels), total_pixels)
            self.score_percentage = self.play_through.note_manager.score / Constants.PlayThrough.Score.TOTAL_SCORE * 100
            self.grade_frame = Constants.Result.Grade.getGradeFrame(
                self.score_percentage)
            self.count = self.play_through.note_manager.counter
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
                pyxel.cls(2 if self.score_percentage >=
                          Constants.Result.Grade.A else 3)
                counter_positions = [
                    util.grid(
                        Constants.Cast.WIDTH, Constants.Cast.HEIGHT, 5, 16, 1 +
                        (x % 2) * 2, 12 + (0 if x < 2 else 1)) for x in range(4)]
                tp_pos = util.grid(Constants.Cast.WIDTH,
                                   Constants.Cast.HEIGHT, 5, 16, 2, 12.5)
                score_pos = util.grid(
                    Constants.Cast.WIDTH, Constants.Cast.HEIGHT, 5, 16, 2, 11)
                count_prop = self.count.get_prop()
                # Average Accuracy
                pyxel.text(*tp_pos, "AA: {0:.2f}%".format(self.tp), 13)
                pyxel.text(*score_pos, f"Score: {self.score}", 14)
                for x in range(4):
                    key = list(count_prop.keys())[x]
                    pyxel.text(
                        *counter_positions[x],
                        f"{key}: {count_prop[key]}", 12 - x)
                self.grade_frame.draw(
                    *Constants.Cast.center(self.grade_frame.width, self.grade_frame.height))
            if self.animating and not self.finished:
                for i in range(Constants.Result.ANIMATION_SPEED):
                    if len(self.animation_bitmap) == 0:
                        self.animating = False
                        self.finished = True
                        break
                    rand = self.animation_bitmap.pop()
                    x = rand % Constants.Cast.WIDTH
                    pos = [(rand - x) / Constants.Cast.WIDTH, x]
                    pyxel.pset(*pos, 0)

        def is_finished(self):
            return self.finished

        def next_cast(self):
            return Casts.LevelSelection()

        def clear_screen(self):
            if not self.animating:
                super().clear_screen()

    class Settings(Cast):

        AVAILABLE_SETTINGS = [
            ["fps", "FPS                      ", "range", [1, 60]],
            ["rel_music_offset", "Relative Music Offset    ", "range", [-1000, 1000]],
            ["full_screen", "Fullscreen               ", "enum_options", [True, False]],
            ["control.up_arrow", "Control: Up    Arrow     ", "control"],
            ["control.down_arrow", "Control: Down  Arrow     ", "control"],
            ["control.left_arrow", "Control: Left  Arrow     ", "control"],
            ["control.right_arrow", "Control: Right Arrow     ", "control"],
            ["control.up_arrow2", "Control: Up    Arrow 2   ", "control"],
            ["control.down_arrow2", "Control: Down  Arrow 2   ", "control"],
            ["control.left_arrow2", "Control: Left  Arrow 2   ", "control"],
            ["control.right_arrow2", "Control: Right Arrow 2   ", "control"],
            ["control.RD_arrow", "Control: Right Down Arrow", "control"],
            ["control.LD_arrow", "Control: Left  Down Arrow", "control"],
            ["control.RU_arrow", "Control: Right Up   Arrow", "control"],
            ["control.LU_arrow", "Control: Left  Up   Arrow", "control"],
            ["control.SEL_L", "Control: Left  Select    ", "control"],
            ["control.SEL_R", "Control: Right Select    ", "control"]
        ]

        def __init__(self):
            self.current_setting = 0
            self.update_selection()
            self.finished = False
            self.is_listening = False

        def update(self):
            if pyxel.btn(pyxel.KEY_Q):
                game_config.GLOB_CONFIG.save()
                self.finished = True  # Skip the starting screen
                return None
            if self.is_listening:
                return None
            if pyxel.btnp(
                    pyxel.KEY_LEFT) or pyxel.btnp(
                    pyxel.KEY_RIGHT) or pyxel.btnp(
                    pyxel.KEY_RIGHT, 30, 2) or pyxel.btnp(
                    pyxel.KEY_LEFT, 30, 2):
                self.current_selection_index += -1 if pyxel.btnp(
                    pyxel.KEY_LEFT) or pyxel.btnp(
                    pyxel.KEY_LEFT, 30, 2) else 1
                if self.current_setting_obj[2] == "enum_options":
                    if self.current_selection_index < 0:
                        self.current_selection_index = len(
                            self.current_setting_obj[-1]) - 1
                    if self.current_selection_index >= len(
                            self.current_setting_obj[-1]):
                        self.current_selection_index = 0
                    self.current_selection = self.current_setting_obj[3][
                        self.current_selection_index]
                elif self.current_setting_obj[2] == "range":
                    if self.current_selection_index < self.current_setting_obj[3][0]:
                        self.current_selection_index = self.current_setting_obj[3][1]
                    elif self.current_selection_index > self.current_setting_obj[3][1]:
                        self.current_selection_index = self.current_setting_obj[3][0]
                    self.current_selection = self.current_selection_index
                game_config.GLOB_CONFIG.config[self.current_setting_obj[0]
                                               ] = self.current_selection
            if pyxel.btnp(
                    pyxel.KEY_UP) or pyxel.btnp(
                    pyxel.KEY_UP, 30, 2) or pyxel.btnp(
                    pyxel.KEY_DOWN) or pyxel.btnp(
                    pyxel.KEY_DOWN, 30, 2):
                self.current_setting += 1 if pyxel.btnp(
                    pyxel.KEY_DOWN) or pyxel.btnp(
                    pyxel.KEY_DOWN, 30, 2) else -1
                if self.current_setting < 0:
                    self.current_setting = len(
                        Casts.Settings.AVAILABLE_SETTINGS) - 1
                elif self.current_setting >= len(Casts.Settings.AVAILABLE_SETTINGS):
                    self.current_setting = 0
                self.update_selection()
            if pyxel.btnr(pyxel.KEY_ENTER):
                if not self.is_listening and self.current_setting_obj[2] == "control":
                    from pynput import keyboard

                    def on_press(key):
                        try:
                            k = key.char  # single-char keys
                        except Exception:
                            k = key.name  # other keys
                        Config.CAST.current_selection = k
                        game_config.GLOB_CONFIG.config[Config.CAST.current_setting_obj[0]
                                                       ] = Config.CAST.current_selection
                        return False  # stop listener; remove this if want more keys

                    listener = keyboard.Listener(on_press=on_press)

                    # FIXME: ??? Raises system error [1]     illegal hardware instruction
                    # This had been tested well before commit 2173962eab28343659bf4c8a0c4f64ba1decd7bc (or maybe even earlier)
                    # This somehow starts to raise a system error?
                    # It happens not only in this commit, but straight to c2f58b56fbec71906336f3f4f8dbaaee9e7b4323 this appears.
                    # However it hadn't been....
                    # Is it my system's thing or what??????????

                    # P.S.: separating code L345-L371 in this commit and run it doesn't raise any errors.
                    # There may be some compatibility issues with other libs...???

                    # P.S.: It just became normal again......

                    listener.start()  # start to listen on a separate thread

        def draw(self):
            pyxel.text(0, 6, "Settings", 12)
            pyxel.text(0, 12, "Changes will be applied on restart", 12)
            index = 4
            for settings in Casts.Settings.AVAILABLE_SETTINGS:
                pyxel.text(
                    0, index * 6,
                    f"{'> ' if self.current_setting_obj[0] == settings[0] else ''}{settings[1]}: {game_config.GLOB_CONFIG.config[settings[0]]}",
                    12)
                index += 1

        def update_selection(self):
            self.current_setting_obj = Casts.Settings.AVAILABLE_SETTINGS[self.current_setting]
            self.current_selection = game_config.GLOB_CONFIG.config[self.current_setting_obj[0]]
            self.current_selection_index = self.current_setting_obj[-1].index(self.current_selection) \
                if self.current_setting_obj[2] == "enum_options" else \
                self.current_selection \
                if self.current_setting_obj[2] == "range" else \
                0

        def is_finished(self):
            return self.finished

        def next_cast(self):
            return Casts.LevelSelection()
