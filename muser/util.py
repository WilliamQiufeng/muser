import errno
import re
import time
import functools
import subprocess
import sys
import os
import io
import zipfile
import shutil


version = "v1.5-pre1"

def copy_multiple(src: list, dest: str):
    for path in src:
        copy(path, dest)
# https://www.pythoncentral.io/how-to-recursively-copy-a-directory-folder-in-python/
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print(f'Directory {src} not copied. Error: %s' % e)
            

def move(src, dest):
    try:
        shutil.move(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        print('Directory not moved. Error: %s' % e)
            
# https://stackoverflow.com/a/31631711/11225486
def humanbytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B  = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1, 048, 576
    GB = float(KB ** 3)  # 1, 073, 741, 824
    TB = float(KB ** 4)  # 1, 099, 511, 627, 776

    if B < KB:
       return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
       return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
       return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
       return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
       return '{0:.2f} TB'.format(B/TB)

# https://code.tutsplus.com/tutorials/compressing-and-extracting-files-in-python--cms-26816
def unzip_files(zip_path: str, out_dir: str):
    zip_file = zipfile.ZipFile(zip_path)
    zip_file.extractall(out_dir)
    zip_file.close()

# https://code.tutsplus.com/tutorials/compressing-and-extracting-files-in-python--cms-26816
def zip_files(output: str, dir: str):
    zip_file = zipfile.ZipFile(output, 'w')
    for folder, subfolders, files in os.walk(dir):
        for file in files:
            zip_file.write(os.path.join(folder, file), os.path.relpath(os.path.join(
                folder, file), dir), compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()

def combine_files(files: list, out_file: str):
    file = io.open(out_file, "wb")
    for piece in files:
        file.write(io.open(piece, "rb").read())
    file.close()
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
