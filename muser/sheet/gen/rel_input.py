import io
from muser.sheet.sheet_constants import *
from muser.sheet.note import *
from muser.sheet.gen.abs_output import *

class SourceSheetInput:
    def __init__(self, file="null"):
        if file != "null":
            self.input = io.open(file, "r");
    def pre(self):
        self.preprocess = eval(self.input.read())
    def process(self):
        if not isinstance(self.preprocess, dict): # The root value must be a dictionary
            raise NotImplementedError
        self.author = self.preprocess["author"] if "author" in self.preprocess.keys() else "Unknown"
        self.music_author = self.preprocess["music_author"] if "music_author" in self.preprocess.keys() else "Unknown"
        self.version = self.preprocess["version"] if "version" in self.preprocess.keys() else "0.0.0.0"
        self.name = self.preprocess["name"] if "name" in self.preprocess.keys() else "Unknown"
        self.level = self.preprocess["level"] if "level" in self.preprocess.keys() else "Normal"
        self.music = self.preprocess["music"] if "music" in self.preprocess.keys(
        ) else "/Unknown"
        self.tempo = self.preprocess["tempo"] if "tempo" in self.preprocess.keys() else 60
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
    
    def process_all(self):
        self.pre()
        self.process()
        self.process_notes(self.preprocess["notes"] if "notes" in self.preprocess.keys() else [])

    def process_notes(self, note_sets):
        cur_beat = 0
        self.abs_notes = []
        tempo = self.tempo
        beat_interval = self.beat_interval
        min_offset = 100000000
        for note_set in note_sets:
            for note in note_set:
                if note.type == NoteType.WAIT:
                    cur_beat += note.length
                elif note.type == NoteType.NOTE:
                    abs_note = AbsNote(cur_beat - note.speed, note.length, note.speed)
                    abs_note.absolutify(beat_interval)
                    min_offset = min(min_offset, abs_note.offset)
                    self.abs_notes.append(abs_note)
                elif note.type == NoteType.TEMPO:
                    #abs_note = ChangeTempo(note.tempo, cur_beat * beat_interval)
                    #self.abs_notes.append(abs_note)
                    beat_interval = 60000 / note.tempo
                    tempo = note.tempo
        self.music_offset = -min_offset if min_offset < 0 else 0
        if min_offset < 0:
            for note in self.abs_notes:
                if isinstance(note, AbsNote):
                    note.offset -= min_offset
        self.abs_notes.sort(key = lambda t: t.offset)#TODO
    def to_abs(self):
        return AbsSheetOutput(self).__repr__()
