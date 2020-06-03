import time
import functools

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

def timeit(within = (-1, -1), without = (-1, -1)):
    """
    func: function to be decorated  
    within: only print result within the range of duration
    """
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            cur = time.time()
            # print(f"{func.__qualname__} ( {args}, {kwargs} )")
            res = func(*args, **kwargs)
            dur = time.time() - cur
            dur_ms = dur * 1000
            if ((within[0] == -1 or dur_ms >= within[0]) and (within[1] == -1 or dur_ms < within[1]) and
                (without[0] == -1 or dur_ms < without[0]) and (without[1] == -1 or dur_ms >= without[1])):
                print(f"Function {func.__qualname__} used {dur_ms}ms")
            return res
        return wrapper
    return actual_decorator
