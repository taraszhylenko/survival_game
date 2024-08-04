from engine.area.deck_maker import AreaDeckMaker
from engine.area.habitat import Habitat
from engine.enum import AreaTextType as at
from engine.evolution.deck_maker import EvolutionDeckMaker
from engine.evolution.animal import Animal
from engine.evolution.hand import Hand
from engine.evolution.herd import Herd
from engine.library import Library
from engine.misc.die import Die
from engine.render import Render
from engine.game_transition import CastAnimal, \
                                   CastTrait, \
                                   DiscardTrait, \
                                   DiscardAnimal, \
                                   SwapAnimals, \
                                   DrawCard, \
                                   PlaceArea, \
                                   RemoveArea, \
                                   UpdateStats, \
                                   TakeItem, \
                                   ConvertFat

class Game:
    def __init__(self, evolution_deck_csv,
                       area_deck_csv,
                       num_players):
        self.edict,  self.edeck, self.edisc, self.eh, self.el = EvolutionDeckMaker.from_csv(evolution_deck_csv)
        self.sadict, self.adeck, self.adisc, self.ah, self.al = AreaDeckMaker.from_csv(area_deck_csv)
        self.edeck.shuffle()
        self.adeck.shuffle()
        self.habitat = Habitat()
        self.die   = Die()
        self.hands = [Hand() for _ in range(num_players)]
        self.herds = [Herd() for _ in range(num_players)]
        self.sdict = dict()
        self.library = Library()
        self.num_players = num_players

    def find_animal_owner(self, card):
        idx = -1
        for i in range(self.num_players):
            if self.herds[i].find_animal_index(card) != -1:
                idx = i
        return idx

    def find_animal_index(self, card):
        o = self.find_animal_owner(card)
        if o == -1:
            return -1
        return self.herds[o].find_animal_index(card) 

    def find_animal(self, card):
        o   = self.find_animal_owner(card)
        idx = self.find_animal_index(card)
        if o != -1 and idx != -1:
            return self.herds[o].get(idx)
        else:
            return -1
    
    def find_trait_owner(self, card):
        idx = -1
        for i in range(self.num_players):
            if self.herds[i].find_trait_index(card) != -1:
                idx = i
        return idx

    def find_hand_owner(self, card):
        idx = -1
        for i in range(self.num_players):
            if self.hands[i].contains(card):
                idx = i
        return idx

    def is_animal(self, card):
        return len(self.find_animal(card)) > 0

    def animal_traits(self, card):
        assert self.is_animal(card)
        return Aimal.traits_txt(self.find_animal(card), self.edict)

    def is_subarea(self, card):
        return self.habitat.contains(card)

    def subarea_name(self, card):
        assert self.is_subarea(card)
        return self.sadict[card].get_text(at.NAME)

    def subarea_has_item(self, card, item_type):
        return self.sdict[card].get(item_type) > 0

    def subarea_accessible(card, target_card):
        assert self.is_animal(card)
        assert self.is_subarea(target_card)
        return self.library.area_accessible(self.animal_traits(card),
                                            self.subarea_name(target_card))

    def can_eat(self, card):
        assert self.is_animal(card)
        a = self.find_animal(card)
        return Animal.num_food(a, self.sdict) + \
               Animal.num_fat(a, self.sdict) < \
               Animal.num_req(a, self.sdict) + \
               Animal.num_fat_capacity(a, self.edict)

    def can_hide(self, card):
        assert self.is_animal(card)
        a = self.find_animal(card)
        return Animal.num_grn(a, self.sdict) == 0 or \
               Animal.has_trait(a, self.edict, 'xylophagous')

    def swap_animals(self, player, card1, card2):
        return self.run_transition(SwapAnimals, {'player': player,
                                                  'card1': card1,
                                                  'card2': card2})

    def draw(self, player):
        return self.run_transition(DrawCard, {'player': player})

    def cast_animal(self, player, card):
        return self.run_transition(CastAnimal, {'player': player,
                                         'card': card})

    def cast_trait(self, player, card, trait_type, target_cards):
        return self.run_transition(CastTrait, {'player': player,
                                        'card': card,
                                        'trait_type': trait_type,
                                        'target_cards': target_cards})

    def discard_animal(self, player, card):
        return self.run_transition(DiscardAnimal, {'player': player,
                                            'card': card})
    
    def discard_trait(self, player, card):
        return self.run_transition(DiscardTrait, {'player': player,
                                           'card': card})

    def run_transition(self, transition_type, args):
        transition = transition_type(args)
        feasible, reason = transition.feasible(self)
        if feasible:
            transition.apply(self)
            return 'ok'
        else:
            return f'Transition infeasible: {reason}'

    def place_area(self):
        return self.run_transition(PlaceArea, {})

    def remove_area(self):
        return self.run_transition(RemoveArea, {})

    def update_stats(self):
        return self.run_transition(UpdateStats, {})

    def convert_fat(self):
        return self.run_transition(ConvertFat, {})

    def take_item(self, player, card, item_type, target_card):
        return self.run_transition(TakeItem, {'player': player,
                                       'card': card,
                                       'item_type': item_type,
                                       'target_card': target_card})

    def render(self):
        self.update_stats()
        self.convert_fat()
        players = Render.merge_column([Render.merge_column([self.hands[i].render(self.edict).add_title_above(f'vvv Player {i} vvv'),
                                                            self.herds[i].render(self.edict),
                                                            self.herds[i].render_stats(self.sdict, self.eh, self.el)]) for i in range(self.num_players)])
        
        areas = Render.merge_row([self.adeck.render(self.sadict).add_title_above(f'Deck: {self.adeck.size()} cards'),
                                  Render.merge_column([self.habitat.render_top_stats(self.sdict, self.ah, self.al),
                                                       self.habitat.render(self.sadict),
                                                       self.habitat.render_bot_stats(self.sdict, self.ah, self.al)]),
                                  self.adisc.render(self.sadict).add_title_above(f'Discard: {self.adisc.size()} cards')])
        evolutions = Render.merge_row([self.edeck.render(self.edict).add_title_above(f'Deck: {self.edeck.size()} cards'),
                                       self.edisc.render(self.edict).add_title_above(f'Discard: {self.edisc.size()} cards')])
        return Render.merge_row([players, Render.merge_column([areas, self.die.render(), evolutions])])

