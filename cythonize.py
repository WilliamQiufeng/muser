import os, io, sys
os.system("rm muser_main.py muser_main.c")
inp = io.open("main.py", "r")
out = io.open("muser_main.py", "w")
out.write("# cython: language_level=3\n")
out.write(inp.read())
out.close()
# os.system("python3 -m cython muser_main.py -3")
# os.system("g++ -c -v -fPIC -I/Users/jessiezhang/.pyenv/versions/3.7-dev/include/python3.7m/ -l/Users/jessiezhang/.pyenv/versions/3.7-dev/lib/libpython3.7m.a muser_main.c")
# os.system("g++ -shared muser_main.o -o muser_main.so")
# os.system("rm muser_main.c muser_main.py muser_main.o")

from distutils.core import setup
from Cython.Build import cythonize
setup(
    ext_modules=cythonize("muser_main.py")
)
