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

    def find_animal_herd(self, card):
        idx = -1
        for i in range(self.num_players):
            if self.herds[i].find_animal_index(card) != -1:
                idx = i
        return idx

    def find_trait_herd(self, card):
        idx = -1
        for i in range(self.num_players):
            if self.herds[i].find_trait_index(card) != -1:
                idx = i
        return idx

    def draw(self, player):
        self.hands[player].add(self.edeck.draw())

    def play_animal(self, player, card):
        self.hands[player].discard(card)
        self.herds[player].cast_animal(card)

    def play_trait(self, player, card, trait_type, target_cards):
        assert len(target_cards) < 3, "can cast up to 2 targets"
        for i, target_card in enumerate(target_cards):
            target_player = self.find_animal_herd(target_card)
            if target_player != -1:
                if i == 0:
                    self.hands[player].discard(card)
                self.herds[target_player].cast_trait(card, trait_type, target_card)
            else:
                raise AssertionError(f"no player has {target_card} in herd")

    def discard_trait(self, player, card):
        discarded = False
        while self.find_trait_herd(card) == player:
            self.herds[player].discard_trait(card)
            discarded = True
        if discarded:
            self.edisc.add(card)

    def discard_animal(self, player, card):
        pass

    def render(self):
        players = Render.merge_column([Render.merge_column([Render.from_string(f'vvv Player {i} vvv'),
                                                            self.hands[i].render(self.edict),
                                                            self.herds[i].render(self.edict)]) for i in range(self.num_players)])

        return players 

