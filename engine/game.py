from engine.misc.die import Die
from engine.render import Render
from engine.arena import Arena

class Game:
    def __init__(self, evolution_manager,
                       area_manager,
                       num_players):
        self.evolution_manager = evolution_manager
        self.area_manager = area_manager
        self.die   = Die()
        self.arena = Arena(num_players)

    def render(self):
        return Render.merge_into_row([self.arena.render(evolution_dict), 
                                      self.die.render()
                                      self.evolution_manager.render()
                                      self.area_manager.render()
                                     ])


