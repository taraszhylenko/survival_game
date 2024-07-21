import pandas as pd
import numpy  as np
import random

from engine.area.card    import AreaCard, SubArea
from engine.misc.counter import Counter
from engine.render import Render
from engine.deck import Deck

class AreaDeck(Deck):
    @staticmethod
    def from_csv(csv_file):
        ad = AreaDeck()
        deck_df = pd.read_csv(csv_file).fillna('').astype({'name1':     str,
                                                          'effect1':   str,
                                                          'back_txt1': str,
                                                          'front_txt1': str,
                                                          'name2':     str,
                                                          'effect2':   str,
                                                          'back_txt2': str,
                                                          'front_txt2': str,
                                                          'quantity':  int})
        assert 'red1'   in deck_df.columns
        assert 'green1' in deck_df.columns
        assert 'red2'   in deck_df.columns
        assert 'green2' in deck_df.columns
        for _, row in deck_df.iterrows():
            for _ in range(row.quantity):
                subareas = []
                subareas.append((row.name1,
                                 row.effect1,
                                 row.red1,
                                 row.green1,
                                 row.back_txt1,
                                 row.front_txt1))
                if row.name2 != '':
                    subareas.append((row.name2,
                                     row.effect2,
                                     row.red2,
                                     row.green2,
                                     row.back_txt2,
                                     row.front_txt2))
                ad.add_card_spec(subareas)
        ad.create_cards()
        ad.shuffle()
        return ad

    def add_card_spec(self, subareas):
        subareas_rendered = list()
        for name, effect, red, green, back_txt, front_txt in subareas:
            back = Render.from_txt(back_txt)
            front = Render.from_txt(front_txt)
            subareas_rendered.append((name, effect, int(red), int(green), back, front))
            self.l = max([self.l, len(name) + 10, len(effect) + 5, back.l + 5, front.l + 5, 12])
            self.h = max([self.h, back.h + 5, front.h + 7])
        self.card_tuples.append(subareas_rendered)

    def create_cards(self):
        idx = 0
        for subareas_rendered in self.card_tuples:
            ac = AreaCard()
            for name, effect, red, green, back, front in subareas_rendered:
                ac.add_subarea(SubArea(name, effect, red, green, back, front, self.h, self.l, idx))
                idx += 1
            self.add_card(ac)
