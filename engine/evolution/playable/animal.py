from engine.evolution.card  import EvolutionCard
from engine.evolution.playable.trait import Trait

class Animal:
    def __init__(self, card, idx):
        assert isinstance(card, EvolutionCard)
        self.card = card
        self.idx  = idx
        self.traits   = list()
    
    def add_trait(self, trait_idx):
        self.traits.append(trait_idx)

    def remove_trait(self, trait_idx):
        self.traits.remove(trait_idx)

    def render(self, trait_dict):
        target = self.card.render_back(f'a{self.idx}')
        for trait_idx in self.traits:
            trait = trait_dict[trait_idx]
            target = target.stack_below(trait.render(), True)
        return target
