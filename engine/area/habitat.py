from engine.render import Render
from engine.area.card import Area

class Habitat:
    def __init__(self):
        self.areas = list()

    def place(self, area):
        self.areas.insert(0, area)

    def size(self):
        return len(self.areas)

    def pop(self):
        return self.areas.pop(-1)

    def render(self, subarea_dict):
        return Render.merge_row([Area.render_front(a, subarea_dict) for a in self.areas])
