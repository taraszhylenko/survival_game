import pandas as pd
import random

from engine.evolution.card import EvolutionCard
from engine.render import Render

class EvolutionDeck:
    def __init__(self):
        self.cards = list()
        self.h = 3
        self.l = 3
        self.card_tuples = list()
        self.cards = list()
    
    @staticmethod
    def from_csv(csv_file):
        ed = EvolutionDeck()
        deck_df = pd.read_csv(csv_file)
        assert 'main_trait' in deck_df.columns
        assert 'short_trait' in deck_df.columns
        assert 'quantity' in deck_df.columns
        assert 'front_txt' in deck_df.columns
        assert 'back_txt' in deck_df.columns
        for _, row in deck_df.iterrows():
            for _ in range(row.quantity):
                ed.add_card_spec(row.main_trait, row.short_trait, row.back_txt, row.front_txt)
        ed.create_cards()
        ed.shuffle()
        return ed


    def add_card_spec(self, main, short, back_txt, front_txt):
        back = Render.from_txt(back_txt)
        front = Render.from_txt(front_txt)
        self.card_tuples.append((main, short, back, front))
        self.l = max([self.l, back.l + 5, len(short) + 10, len(main) + 10, front.l + 5])
        self.h = max([self.h, back.h + 5, front.h + 7])

    def add_card(self, card):
        self.cards.append(card)

    def create_cards(self):
        for main, short, back, front in self.card_tuples:
            self.cards.append(EvolutionCard(main, short, back, front, self.h, self.l))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(-1)

    def render(self):
        return Render.blank(self.h - 2, self.l - 2).add_border(False)

    def render_last_card(self):
        if len(self.cards) > 0:
            return self.cards[-1].render_front('', '')
        else:
            return self.render()
