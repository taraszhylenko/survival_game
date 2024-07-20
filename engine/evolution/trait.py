from engine.evolution.card import EvolutionCard

class Trait:
    def __init__(self, card, side, idx):
        assert isinstance(card, EvolutionCard)
        assert side in {'main', 'short'}
        self.card = card
        self.side = side
        self.idx  = idx

    def render(self):
        if self.side == 'main':
            return self.card.render_main(f't{self.idx}')
        else:
            return self.card.render_short(f't{self.idx}')
