from engine.evolution.card  import EvolutionCard
from engine.evolution.playable.trait import Trait

class Animal:
    def __init__(self, card, idx, slot_idx):
        assert isinstance(card, EvolutionCard)
        self.card = card
        self.idx  = idx
        self.slot_idx = slot_idx
        self.solo_traits   = list()
        self.paired_traits = list()
    
    def add_solo_trait(self, trait_idx):
        self.solo_traits.append(trait_idx)

    def remove_solo_trait(self, trait_idx):
        self.solo_traits.remove(trait_idx)

    def add_paired_trait(self, trait_idx):
        self.paired_traits.append(trait_idx)

    def remove_paired_trait(self, trait_idx):
        self.paired_traits.remove(trait_idx)

    def render(self, trait_dict):
        target = self.card.render_back(f'a{self.idx}')
        for trait_idx in self.solo_traits:
            trait = trait_dict[trait_idx]
            target = target.stack_below(trait.render(), True)
        return target
