import pandas as pd
import random

from engine.misc.counter import Counter
from engine.render import Render

class Deck:
    def __init__(self):
        self.cards = list()

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        assert len(self.cards) > 0, "Can't draw from empty deck"
        return self.cards.pop(-1)

    def render(self, card_dict):
        assert len(self.cards) > 0
        return card_dict[self.cards[-1]].render_back(False)
