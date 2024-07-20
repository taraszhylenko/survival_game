import pandas as pd
import random

from engine.area.card    import AreaCard
from engine.misc.counter import Counter
from engine.render import Render

class Deck:
    def __init__(self):
        self.cards = list()
        self.h = 3
        self.l = 3
        self.card_tuples = list()
        self.card_counter = Counter('cards_left', 0)

    def add_card(self, card):
        self.cards.append(card)
        self.card_counter.increment()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        self.card_counter.decrement()
        return self.cards.pop(-1)

    def render(self):
        return self.card_counter.render().balloon_to(self.h - 2, self.l - 2).add_border(False)

    def render_last_card(self):
        if len(self.cards) > 0:
            return self.cards[-1].render_front()
        else:
            return self.render()
