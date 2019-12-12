from sheet.sheet_constants import *
import random
class AbsSheetOutput:
    def __init__(self, rel_in):
        self.rel_in = rel_in
    def __repr__(self):
        NEWLINE = "\n"
        return "#".join(
            [str(ele) for ele in [
                self.rel_in.author,
                self.rel_in.music_author,
                self.rel_in.version,
                self.rel_in.name,
                self.rel_in.music,
                self.rel_in.music_offset,
                self.rel_in.level,
                NEWLINE.join([str(x) for x in self.rel_in.abs_notes])
            ]]
        )

class AbsNote:
    def __init__(self, offset, beat = 0, pass_time = 2000, absolutified = False, side = random.randint(0, 3)):
        self.offset = offset
        self.beat = beat
        self.pass_time = pass_time
        self.side = side
        self.absolutified = absolutified
    def absolutify(self, beat_interval):
        if not self.absolutified:
            self.offset *= beat_interval
            self.beat *= beat_interval
            self.pass_time *= beat_interval
            self.absolutified = True
    def __repr__(self):
        return f"{NoteType.NOTE},{self.offset},{self.beat},{self.pass_time},{self.side}"
class ChangeTempo:
    """
    tempo: tempo to be set
    time:  time
    """
    def __init__(self, tempo, offset):
        self.tempo = tempo
        self.beat_interval = 60000 / self.tempo
        self.offset = offset
    def __repr__(self):
        return f"{NoteType.TEMPO},{self.offset},{self.tempo},{self.beat_interval}"    
    
