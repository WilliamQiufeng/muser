class AbsSheetOutput:
    def __init__(self, rel_in):
        self.rel_in = rel_in

    def __repr__(self):
        return {
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

    def do_func(self):
        pass

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
    def absolutify(self, beat_interval):
        if not self.absolutified:
            self.offset *= beat_interval
            self.beat *= beat_interval
            self.pass_time *= beat_interval
            self.absolutified = True


class StartFancy(BaseAbsNote):
    pass


class EndEffect(BaseAbsNote):
    pass


class StartFrame(BaseAbsNote):
    def do_func(self):
        self.frame = [[self.substitution[self.frame[line][char_i]]
                       for char_i in range(self.size[0])]
                      for line in range(self.size[1])]


class StartMove(BaseAbsNote):
    pass


class StartCriteria(BaseAbsNote):
    pass
