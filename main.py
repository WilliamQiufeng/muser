import pyxel
pyxel.init(256, 256,
           caption="Muser", scale=48)
print("Window loaded")
pyxel.load("assets/resources.pyxres")
print("Res loaded")
from game import *