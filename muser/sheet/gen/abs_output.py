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
                NEWLINE.join([x.__repr__() for x in self.rel_in.abs_notes])
            ]]
        )

class AbsNote:
    def __init__(self, offset, beat=0, pass_time=2000, side=random.randint(0, 3), absolutified=False):
        self.offset = offset
        self.beat = beat
        self.pass_time = pass_time
        self.side = int(side)
        self.absolutified = absolutified
    def absolutify(self, beat_interval):
        if not self.absolutified:
            self.offset *= beat_interval
            self.beat *= beat_interval
            self.pass_time *= beat_interval
            self.absolutified = True
    def __repr__(self):
        return f"{NoteType.NOTE},{self.offset},{self.beat},{self.pass_time},{self.side}"
class StartFancy:
    def __init__(self, offset: int, colors = [9, 10], interval: float = 250, identity: int = 0, offset_pos: list = [0, 0], size: list = [256, 256]):
        self.offset = offset
        self.colors = colors
        self.interval = interval
        self.identity = identity
        self.offset_pos = offset_pos
        self.size = size
    def __repr__(self):
        return f"{NoteType.FANCY},{self.offset},{';'.join([str(c) for c in self.colors])},{self.interval},{self.identity},{';'.join([str(x) for x in self.offset_pos])},{';'.join([str(x) for x in self.size])}"
class EndEffect:
    def __init__(self, offset: float, identity: int = 0):
        self.offset = offset
        self.identity = identity
    def __repr__(self):
        return f"{NoteType.STOP_EFFECT},{self.offset},{self.identity}"

class StartFrame:
    def __init__(self, offset: float, size: list, frame_list: list, substitution: dict, offset_pos: list = [0, 0], identity: int = 0, substitute: bool = True):
        self.offset = offset
        if substitute:
            self.frame = [[substitution[frame_list[line][char_i]] for char_i in range(size[0])] for line in range(size[1])]
        else:
            self.frame = frame_list
        self.identity = identity
        self.size = size
        self.offset_pos = offset_pos
    def __repr__(self):
        return f"{NoteType.START_FRAME},{self.offset},{';'.join([str(x) for x in self.size])},"\
                f"{';'.join([';'.join([str(col) for col in line]) for line in self.frame])},{';'.join([str(x) for x in self.offset_pos])},{self.identity}"
        
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
    
