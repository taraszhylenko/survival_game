import pandas as pd
import random

from engine.evolution.card import EvolutionCard
from engine.misc.counter import Counter
from engine.render import Render
from engine.deck   import Deck

class EvolutionDeck(Deck):
    @staticmethod
    def from_csv(csv_file):
        ed = EvolutionDeck()
        deck_df = pd.read_csv(csv_file)
        assert 'main_trait' in deck_df.columns
        assert 'main_food_req' in deck_df.columns
        assert 'short_trait' in deck_df.columns
        assert 'short_food_req' in deck_df.columns
        assert 'quantity' in deck_df.columns
        assert 'front_txt' in deck_df.columns
        assert 'back_txt' in deck_df.columns
        for _, row in deck_df.iterrows():
            for _ in range(row.quantity):
                ed.add_card_spec(row.main_trait, row.short_trait,
                                 row.back_txt, row.front_txt, 
                                 {'main': row.main_food_req, 'short': row.short_food_req})
        ed.create_cards()
        ed.shuffle()
        return ed


    def add_card_spec(self, main, short, back_txt, front_txt, reqs):
        back = Render.from_txt(back_txt)
        front = Render.from_txt(front_txt)
        self.card_tuples.append((main, short, back, front, reqs))
        self.l = max([self.l, back.l + 5, len(short) + 10, len(main) + 10, front.l + 5, 12])
        self.h = max([self.h, back.h + 5, front.h + 7])

    def create_cards(self):
        for main, short, back, front, reqs in self.card_tuples:
            new_card = EvolutionCard(main, short, back, front, self.h, self.l, reqs)
            self.add_card(new_card)


