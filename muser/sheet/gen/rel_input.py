import io
from sheet.gen.abs_output import AbsSheetOutput


class SourceSheetInput:
    def __init__(self, file="null"):
        if file != "null":
            self.input = io.open(file, "r")

    def pre(self):
        self.preprocess = eval(self.input.read())

    def process(self):
        if not isinstance(
                self.preprocess, dict):  # The root value must be a dictionary
            raise NotImplementedError
        self.author = self.preprocess["author"] if "author" in self.preprocess.keys(
        ) else "Unknown"
        self.music_author = self.preprocess["music_author"] if "music_author" in self.preprocess.keys(
        ) else "Unknown"
        self.version = self.preprocess["version"] if "version" in self.preprocess.keys(
        ) else "0.0.0.0"
        self.name = self.preprocess["name"] if "name" in self.preprocess.keys(
        ) else "Unknown"
        self.level = self.preprocess["level"] if "level" in self.preprocess.keys(
        ) else "Normal"
        self.music = self.preprocess["music"] if "music" in self.preprocess.keys(
        ) else "/Unknown"
        self.tempo = self.preprocess["tempo"] if "tempo" in self.preprocess.keys(
        ) else 60
        self.effects = self.preprocess["effects"] if "effects" in self.preprocess.keys() else [
        ]
        self.music_offset = self.preprocess["music_offset"] if "music_offset" in self.preprocess.keys(
        ) else 0

        # Calculate the length of a beat
        #                        1 (min)                1000 (ms)
        #  60 (sec) * ------------------------------- * ---------
        #             self.tempo (beat/min) * 1 (min)    1 (sec)
        #
        #                     1 (min)
        # = 60000 (ms) * -----------------
        #                self.tempo (beat)
        #      60000 (ms)
        # = -----------------
        #   self.tempo (beat)
        self.beat_interval = 60000 / self.tempo

    def to_abs(self):
        return AbsSheetOutput(self).__repr__()
