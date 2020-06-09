from sheet.sheet_constants import *
from util import AttrDict
import random
import json
class AbsSheetOutput:
    def __init__(self, rel_in):
        self.rel_in = rel_in
    def __repr__(self):
        NEWLINE = "\n"
        return  {
                "author": self.rel_in.author,
                "music_author": self.rel_in.music_author,
                "version": self.rel_in.version,
                "name": self.rel_in.name,
                "music": self.rel_in.music,
                "music_offset": self.rel_in.music_offset,
                "level": self.rel_in.level,
                "notes": [x.__repr__() for x in self.rel_in.abs_notes]
        }

class BaseAbsNote:
    def __init__(self, prop: dict):
        self.prop = prop
        self.prop["type"] = self.__class__.__name__
    def __getattr__(self, name):
        if name in dir(self):
            return self.__dict__[name]
        else:
            return self.__dict__["prop"][name]
    def __setattr__(self, name, value):
        if name in dir(self):
            self.__dict__[name] = value
        elif name == "prop":
            self.__dict__["prop"] = value
        else:
            self.__dict__["prop"][name] = value
    def __repr__(self):
        return self.prop

class AbsNote(BaseAbsNote):
    # def __init__(self, offset, beat=0, pass_time=2000, side=random.randint(0, 3), absolutified=False):
    def absolutify(self, beat_interval):
        if not self.absolutified:
            self.offset *= beat_interval
            self.beat *= beat_interval
            self.pass_time *= beat_interval
            self.absolutified = True
    # def __repr__(self):
    #     # return f"{NoteType.NOTE},{self.offset},{self.beat},{self.pass_time},{self.side}"
    #     return {
    #         "type": self.__class__.__name__,
    #         "offset": self.offset,
    #         "beat": self.beat,
    #         "pass_time": self.pass_time,
    #         "side": self.side,
    #         "absolutified": self.absolutified
    #     }
class StartFancy(BaseAbsNote):
    # def __init__(self, offset: int, colors = [9, 10], interval: float = 250, identity: int = 0, offset_pos: list = [0, 0], size: list = [256, 256]):
    #     self.offset = offset
    #     self.colors = colors
    #     self.interval = interval
    #     self.identity = identity
    #     self.offset_pos = offset_pos
    #     self.size = size
    # def __repr__(self):
    #     return f"{NoteType.FANCY},{self.offset},{';'.join([str(c) for c in self.colors])},{self.interval},{self.identity},{';'.join([str(x) for x in self.offset_pos])},{';'.join([str(x) for x in self.size])}"
    pass
class EndEffect(BaseAbsNote):
    # def __init__(self, offset: float, identity: int = 0):
    #     self.offset = offset
    #     self.identity = identity
    # def __repr__(self):
    #     return f"{NoteType.STOP_EFFECT},{self.offset},{self.identity}"
    pass
class StartFrame(BaseAbsNote):
    # def __init__(self, offset: float, size: list, frame_list: list, substitution: dict, offset_pos: list = [0, 0], identity: int = 0, substitute: bool = True):
    #     self.offset = offset
    #     if substitute:
    #         self.frame = [[substitution[frame_list[line][char_i]] for char_i in range(size[0])] for line in range(size[1])]
    #     else:
    #         self.frame = frame_list
    #     self.identity = identity
    #     self.size = size
    #     self.offset_pos = offset_pos
    # def __repr__(self):
    #     return f"{NoteType.START_FRAME},{self.offset},{';'.join([str(x) for x in self.size])},"\
    #             f"{';'.join([';'.join([str(col) for col in line]) for line in self.frame])},{';'.join([str(x) for x in self.offset_pos])},{self.identity}"
    def flatten_frame(self):
        self.frame = [[self.substitution[self.frame[line][char_i]]
                       for char_i in range(self.size[0])] for line in range(self.size[1])]
        
class StartMove(BaseAbsNote):
    pass

class StartCriteria(BaseAbsNote):
    pass
