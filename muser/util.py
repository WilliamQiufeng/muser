import re
import time
import functools
import subprocess
import sys


version = "1.5"

# GEEZ A LOT OF COPYING LOL

# https://stackoverflow.com/a/50255019/11225486
def pip_install(package: list):
    args = [sys.executable, "-m", "pip", "install", *package]
    print(" ".join(args))
    subprocess.check_call(args)

# Copied and modified from https://stackoverflow.com/a/8217646/11225486
def cmd(args: list):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=None)
    text = p.stdout.read()
    retcode = p.wait()
    return (str(text.decode('utf-8')), retcode)

# https://geeksforgeeks.org/python-check-url-string/
def find_links(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

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
            res    = func(*args, **kwargs)
            dur    = time.time() - cur
            dur_ms = dur * 1000
            if ((within[0] == -1 or dur_ms >= within[0]) and (within[1] == -1 or dur_ms < within[1]) and
                (without[0] == -1 or dur_ms < without[0]) and (without[1] == -1 or dur_ms >= without[1])):
                print(f"Function {func.__qualname__} used {dur_ms}ms")
            return res
        return wrapper
    return actual_decorator
