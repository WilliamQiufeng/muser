from game.ui import *
import pyxel

def empty_function():
    pass

class KeyListener:
    def __init__(self, key, on_click=empty_function, on_touch=empty_function, not_on_touch = empty_function):
        self.key = key
        self.on_click = on_click
        self.on_touch = on_touch
        self.not_on_touch = not_on_touch
        self.last_state = False
    def update(self):
        self.pressed = pyxel.btn(self.key)
        if self.pressed:
            if self.last_state != self.pressed:
                self.on_touch()
        else:
            self.not_on_touch()
            if self.last_state:
                self.on_click()
        self.last_state = self.pressed
class Button(Widget):
    def __init__(self, x, y, key, ot_frame, not_frame, on_click = empty_function, on_touch = empty_function):
        self.x = x
        self.y = y
        self.listener = KeyListener(key, on_click, on_touch)
        self.ot_frame = ot_frame
        self.not_frame = not_frame
        self.cur_frame = not_frame
        self.last_state = False
    def update(self):
        self.listener.update()
        self.cur_frame = self.ot_frame if self.listener.pressed else self.not_frame
    def draw(self):
        self.cur_frame.draw(self.x, self.y)
