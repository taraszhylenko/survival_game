from engine.area.deck_maker import AreaDeckMaker
from engine.area.habitat import Habitat
from engine.evolution.deck_maker import EvolutionDeckMaker
from engine.evolution.hand import Hand
from engine.evolution.herd import Herd
from engine.misc.die import Die
from engine.render import Render
from engine.game_transition import CastAnimal, \
                                   CastTrait, \
                                   DiscardTrait, \
                                   DiscardAnimal, \
                                   SwapAnimals, \
                                   DrawCard, \
                                   PlaceArea, \
                                   RemoveArea

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
        self.num_players = num_players

    def draw(self, player):
        self.run_transition(DrawCard, {'player': player})

    def cast_animal(self, player, card):
        self.run_transition(CastAnimal, {'player': player,
                                         'card': card})

    def cast_trait(self, player, card, trait_type, target_cards):
        self.run_transition(CastTrait, {'player': player,
                                        'card': card,
                                        'trait_type': trait_type,
                                        'target_cards': target_cards})

    def discard_animal(self, player, card):
        self.run_transition(DiscardAnimal, {'player': player,
                                            'card': card})
    
    def discard_trait(self, player, card):
        self.run_transition(DiscardTrait, {'player': player,
                                           'card': card})

    def run_transition(self, transition_type, args):
        transition = transition_type(args)
        feasible, reason = transition.feasible(self)
        if feasible:
            transition.apply(self)
        else:
            print(f'Transition infeasible: {reason}')

    def place_area(self):
        self.run_transition(PlaceArea, {})

    def remove_area(self):
        self.run_transition(RemoveArea, {})

    def render(self):
        players = Render.merge_column([Render.merge_column([self.hands[i].render(self.edict).add_title_above(f'vvv Player {i} vvv'),
                                                            self.herds[i].render(self.edict),
                                                            self.herds[i].render_stats(self.sdict, self.eh, self.el)]) for i in range(self.num_players)])
        
        areas = Render.merge_row([self.adeck.render(self.sadict).add_title_above(f'Deck: {self.adeck.size()} cards'),
                                  self.habitat.render(self.sadict),
                                  self.adisc.render(self.sadict).add_title_above(f'Discard: {self.adisc.size()} cards')])
        evolutions = Render.merge_row([self.edeck.render(self.edict).add_title_above(f'Deck: {self.edeck.size()} cards'),
                                       self.edisc.render(self.edict).add_title_above(f'Discard: {self.edisc.size()} cards')])
        return Render.merge_row([players, Render.merge_column([areas, self.die.render(), evolutions])])

