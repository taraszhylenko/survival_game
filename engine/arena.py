from engine.render import Render
from engine.evolution.playable.animal import Animal

class Arena:
    def __init__(self, num_players):
        self.players  range(num_players)
        self.hands    = {p: list() for p in self.players}
        self.animals  = {p: list() for p in self.players}
        self.stats    = dict()

    def draw(self, player):
        pass

    def cast_animal(self, player, card):
        pass

    def cast_trait(self, player, card, trait_type, target_card):
        pass

    def discard_trait(self, card):
        pass

    def discard_animal(self, card):
        pass

    def swap_animals(self, player, card1, card2):
        pass

    def update_stats(self):
        pass

    def find_traits(self, card):
        pass

    def render_animals(self, player):
        pass

    def render_animal(self, card):
        pass

    def render_stats(self, card):
        pass

    def render_hand(self, player)
        pass

    def render_player(self, player):
        pass

    def render(self)
        return Render.merge_into_column([self.render_player[p] for p in self.players])
