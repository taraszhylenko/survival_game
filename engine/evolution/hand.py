from engine.render import Render
from engine.evolution.animal import Animal

class Hand:
    def __init__(self):
        self.cards = list()

    def add(self, card):
        self.cards.append(card)

    def find_index(self, card):
        idx = -1
        if card in self.cards:
            idx = self.cards.index(card)
        return idx

    def discard(self, card):
        idx = self.find_index(card)
        assert idx != -1
        self.cards.pop(idx)

    def render(self, card_dict):
        return Render.merge_row([card_dict[c].render_front(True) for c in self.cards])
