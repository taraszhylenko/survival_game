from engine.deck import Deck
from engine.evolution.card import EvolutionCard

class EvolutionDeckMaker:
    @static_method
    def from_csv(csv_file):
        deck_df = pd.read_csv(csv_file)
        assert 'main_trait' in deck_df.columns
        assert 'short_trait' in deck_df.columns
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
        ed = Deck()
        for _, row in deck_df.iterrows():
            for _ in range(row.quantity):
                main  = row.main
                short = row.short
                back = Render.from_txt(row.back_txt).balloon_to(h - 2, l - 2).add_border(False)
                front = Render.from_txt(row.front_txt).balloon_to(h - 4, l - 2).add_border(False)
                card = EvolutionCard([main, short], [back, front], h, l, idx)
                idx += 1
                ed.add_card(card)
        return ed
                


