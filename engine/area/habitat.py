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

    def render_top_stats(self, stat_dict, h, l):
        stats = [stat_dict[a[0]].render() if len(a) == 2 else Render.blank(1, 1) for a in self.areas]
        return Render.merge_row([stat.balloon_to(stat.h, l) for stat in stats])

    def contains(self, card):
        return any([card in area for area in self.areas])

    def render_bot_stats(self, stat_dict, h, l):
        stats = [stat_dict[a[1]].render() if len(a) == 2 else stat_dict[a[0]].render() for a in self.areas]
        return Render.merge_row([stat.balloon_to(stat.h, l) for stat in stats])
