from engine.evolution.card import EvolutionCard
from engine.evolution.playable.animal import Animal
from engine.evolution.playable.trait  import Trait
from engine.misc.die import Die
from engine.render import Render

class Board:
    def __init__(self, evolution_deck,
                       evolution_discard,
                       area_deck,
                       area_discard):
        self.evolution_deck = evolution_deck
        self.evolution_discard = evolution_discard 
        self.area_deck = area_deck
        self.die = Die()
        self.animal_dict = dict()
        self.animal_ctr  = 0
        self.trait_dict  = dict()
        self.trait_ctr   = 0
        self.animal_rows = [[], []]
        self.area_row    = [[], []]

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
        self.trait_dict[trait_idx] = trait
        self.animal_dict[animal_idx].add_trait(trait_idx, self.trait_dict)
        self.trait_ctr += 1

    def discard_trait(self, trait_idx):
        for animal in self.animal_dict.values():
            animal.remove_trait(trait_idx, self.trait_dict)
        self.evolution_discard.add_card(self.trait_dict[trait_idx].card)
        del self.trait_dict[trait_idx]

    def discard_animal(self, animal_idx):
        for trait_idx in self.animal_dict[animal_idx].traits:
            self.discard_trait(trait_idx)
        for i in range(2):
            if animal_idx in self.animal_rows[i]:
                self.animal_rows[i].pop(self.animal_rows[i].index(animal_idx))
        self.evolution_discard.add_card(self.animal_dict[animal_idx].card) 
        del self.animal_dict[animal_idx]

    def render(self):
        row0 = Render.merge_into_row([Render.blank(1, 1)] + [self.animal_dict[i].render(self.trait_dict) for i in self.animal_rows[0]])
        divider = Render.merge_into_column([Render.from_string('^^^ PLAYER 1 ^^^'),
                                            Render.from_string('vvv PLAYER 2 VVV')])
        row1 = Render.merge_into_row([Render.blank(1, 1)] + [self.animal_dict[i].render(self.trait_dict) for i in self.animal_rows[1]])
        animals = Render.merge_into_column([row0, divider, row1])
        divider2 = Render.from_string("<<< ANIMALS | DECKS >>>")
        utilities = Render.merge_into_column([self.evolution_deck.render(),
                                              self.evolution_discard.render_last_card(),
                                              self.die.render()]
                                              )
        return Render.merge_into_row([animals, divider2, utilities])


    def reveal_area(self):
        pass

    def discard_area(self):
        pass

    def populate_areas(self):
        pass
