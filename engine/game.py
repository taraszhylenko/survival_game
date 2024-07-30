from engine.area.deck_maker import AreaDeckMaker
from engine.area.habitat import Habitat
from engine.evolution.deck_maker import EvolutionDeckMaker
from engine.evolution.hand import Hand
from engine.evolution.herd import Herd
from engine.misc.die import Die
from engine.render import Render

class Game:
    def __init__(self, evolution_deck_csv,
                       area_deck_csv,
                       num_players):
        self.edict,  self.edeck, self.edisc = EvolutionDeckMaker.from_csv(evolution_deck_csv)
        self.sadict, self.adeck, self.adisc = AreaDeckMaker.from_csv(area_deck_csv)
        self.edeck.shuffle()
        self.adeck.shuffle()
        self.habitat = Habitat()
        self.die   = Die()
        self.hands = [Hand() for _ in range(num_players)]
        self.herds = [Herd() for _ in range(num_players)]
        self.num_players = num_players

    def run_transition(self, transition, args):
        transition.init(args)
        feasible, reason = transition.feasible(self)
        if feasible:
            transition.apply(self)
        else:
            print(f'Transition infeasible: {reason}')

    def render(self):
        players = Render.merge_column([Render.merge_column([Render.from_string(f'vvv Player {i} vvv'),
                                                            self.hands[i].render(self.edict),
                                                            self.herds[i].render(self.edict)]) for i in range(self.num_players)])

        return players 

