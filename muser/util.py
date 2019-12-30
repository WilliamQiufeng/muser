def grid(sw, sh, gw, gh, x, y):
    gridw = sw / gw
    gridh = sh / gh
    return (gridw * x, gridh * y)
class AttrDict:
    def __init__(self, obj: dict):
        self.obj = obj
    def __getattribute__(self, name):
        return self.obj[name]
    def __setattr__(self, name, value):
        self.obj[name] = value
        return self