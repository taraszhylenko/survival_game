from engine.evolution.playable.animal import Animal
from engine.evolution.playable.trait  import Trait
from engine.misc.die import Die

class Board:
    def __init__(self, evolution_deck, area_deck):
        self.evolution_deck = e_deck
        self.evolution_discard = list() 
        self.area_deck = a_deck
        self.die = Die()
        self.animal_dict = dict()
        self.animal_ctr  = 0
        self.trait_dict  = dict()
        self.trait_ctr   = 0
        self.animal_rows = [[], []]

    def cast_animal(self, card, row):
        assert isinstance(card, EvolutionCard)
        assert isinstance(row, int)
        assert 0 <= row < 2
        animal_idx = self.animal_ctr
        animal = Animal(card, animal_idx)
        self.animal_dict[animal_idx] = animal
        self.animal_ctr += 1
        self.animal_rows[row].append(animal_idx)

    def cast_trait(self, card, side, animal_idx):
        assert isinstance(card, EvolutionCard)
        assert side in {'main', 'short'}
        assert animal_idx in self.animal_dict
        trait_idx = self.trait_ctr 
        trait = Trait(card, side, trait_idx)
        self.animal_dict[animal_idx].add_trait(trait_idx)
        self.trait_ctr += 1

    def discard_trait(self, trait_idx):
        for animal in animal_dict.values():
            if trait_idx in animal.traits:
                animal.traits.pop(animal.traits.index(trait_idx))
        self.evolution_discard.append(self.trait_dict[trait_idx].card)
        del self.trait_dict[trait_idx]

    def discard_animal(self, animal_idx):
        for trait_idx in self.animal_dict[animal_idx].traits:
            self.discard_trait(trait_idx)
        for i in range(2):
            if animal_idx in self.animal_rows[i]:
                discarded_animal = self.animal_rows[i].pop(self.animal_rows[i].index(animal_idx))
                self.evolution_discard.append(discarded_animal.card) 

