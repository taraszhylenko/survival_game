import pandas as pd

from engine.evolution.card import EvolutionCard
from engine.deck import Deck
from engine.render import Render

class EvolutionDeckMaker:
    @staticmethod
    def from_csv(csv_file):
        deck_df = pd.read_csv(csv_file).sample(frac=1)
        assert 'main' in deck_df.columns
        assert 'short' in deck_df.columns
        assert 'quantity' in deck_df.columns
        assert 'front_txt' in deck_df.columns
        assert 'back_txt' in deck_df.columns
        l = 0
        h = 0
        for _, row in deck_df.iterrows():
            main  = row.main
            short = row.short
            back = Render.from_txt(row.back_txt)
            front = Render.from_txt(row.front_txt)
            l = max([l, back.l + 2, front.l + 2, len(short) + 6, len(main) + 6, 13])
            h = max([h, back.h + 2, front.h + 4])

        idx = 0
        evolution_dict = dict()
        evolution_deck = Deck()
        for _, row in deck_df.iterrows():
            for _ in range(row.quantity):
                main  = row.main
                short = row.short
                back = Render.from_txt(row.back_txt).balloon_to(h - 2, l - 2).add_border(False)
                front = Render.from_txt(row.front_txt).balloon_to(h - 4, l - 2).add_border(False)
                card = EvolutionCard([main, short], [back, front], h, l, str(idx))
                evolution_dict[idx] = card
                evolution_deck.add_card(idx)
                idx += 1
        return evolution_dict, evolution_deck
