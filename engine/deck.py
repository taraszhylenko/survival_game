import pandas as pd
import random

from engine.enum import DeckType
from engine.misc.counter import Counter
from engine.render import Render

class Deck:
    def __init__(self, deck_type):
        self.things = list()
        self.type = deck_type

    def add(self, thing):
        self.things.append(thing)

    def shuffle(self):
        random.shuffle(self.things)

    def draw(self):
        assert len(self.things) > 0, "Can't draw from empty deck"
        return self.things.pop(-1)

    def render(self, thing_dict):
        assert len(self.things) > 0
        if self.type == DeckType.EVOLUTION:
            return thing_dict[self.things[-1]].render_back(False)
        elif self.type == DeckType.AREA:
            return thing_dict[self.things[-1][0]].render_back(False)
