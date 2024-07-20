from engine.evolution.card  import EvolutionCard
from engine.evolution.playable.trait import Trait
from engine.misc.counter import Counter
from engine.render import Render

class Animal:
    def __init__(self, card, idx):
        assert isinstance(card, EvolutionCard)
        self.card = card
        self.idx  = idx
        self.traits   = list()
        self.req = Counter('req', 1)
        self.fat = Counter('fat', 0)
        self.red = Counter('red', 0)
        self.blu = Counter('blu', 0)
    
    def add_trait(self, trait_idx, trait_dict):
        self.traits.append(trait_idx)
        for _ in range(trait_dict[trait_idx].req()):
            self.req.increment()

    def remove_trait(self, trait_idx, trait_dict):
        if trait_idx in self.traits:
            for _ in range(trait_dict[trait_idx].req()):
                self.req.decrement()
        self.traits = list(filter(lambda x: x != trait_idx, self.traits))

    def render(self, trait_dict):
        reqfat = Render.merge_into_column([self.req.render(), 
                                           self.fat.render()])
        redblu = Render.merge_into_column([self.red.render(),
                                           self.blu.render()])
        foods = Render.merge_into_row([reqfat, 
                                       Render.blank(1, 1),
                                       redblu])
        target = self.card.render_back(f'a{self.idx}')
        for trait_idx in self.traits:
            trait = trait_dict[trait_idx]
            target = target.stack_below(trait.render(), True)
        return Render.merge_into_column([target, foods])
