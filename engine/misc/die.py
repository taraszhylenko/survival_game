import random

from engine.render import Render

class Die:
    def __init__(self):
        self.val = random.randint(1, 6)

    def roll(self):
        self.val = random.randint(1, 6)
        return self.val

    def render(self):
        return Render.from_string(f'{self.val}').add_border(False)
