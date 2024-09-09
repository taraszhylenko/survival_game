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

    def contains(self, card):
        return card in self.cards

    def discard(self, card):
        idx = self.find_index(card)
        assert idx != -1, f"player doesn't have {card} in hand"
        self.cards.pop(idx)

    def render(self, card_dict, visible):
        if visible:
            return Render.merge_row([card_dict[c].render_front(True) for c in self.cards])
        else:
            return Render.merge_row([card_dict[c].render_back(False) for c in self.cards])
