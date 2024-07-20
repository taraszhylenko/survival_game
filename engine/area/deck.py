import pandas as pd
import random

from engine.area.card    import AreaCard
from engine.misc.counter import Counter
from engine.render import Render
from engine.deck import Deck

class AreaDeck(Deck):
    @staticmethod
    def from_csv(csv_file):
        ad = AreaDeck()
        deck_df = pd.read_csv(csv_file)
        assert 'quantity' in deck_df.columns
        for _, row in deck_df.iterrows():
            pass
        ad.create_cards()
        ad.shuffle()
        ad.get_top_6()
        return ad

    def create_cards(self):
        pass
