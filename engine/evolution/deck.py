import pandas as pd
import random

from engine.evolution.card import EvolutionCard
from engine.misc.counter import Counter
from engine.render import Render
from engine.deck   import Deck

class EvolutionDeck:
    @staticmethod
    def from_csv(csv_file):
        ed = EvolutionDeck()
        idx = 0
        ed.create_cards()
        ed.shuffle()
        return ed


    def add_card_spec(self, main, short, back_txt, front_txt, reqs):
        self.card_tuples.append((main, short, back, front, reqs))

    def create_cards(self):
        for main, short, back, front, reqs in self.card_tuples:
            new_card = EvolutionCard(main, short, back, front, self.h, self.l, reqs)
            self.add_card(new_card)


