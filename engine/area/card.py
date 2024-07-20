from engine.misc.counter import Counter
from engine.render import Render

class SubArea:
    def __init__(self, name, effect, red, green, back, front, h, l, idx):
        self.name   = name
        self.effect = effect
        self.red    = Counter('red', red)
        self.grn    = Counter('grn', green)
        self.back   = back
        self.front  = front
        self.h = h
        self.l = l
        self.idx = idx
        self.checks()

    def checks(self):
        assert isinstance(self.back,  Render)
        assert isinstance(self.front, Render)
        assert self.l > len(self.name) + 9
        assert self.l > len(self.effect) + 4
        assert self.l > self.back.l + 4 
        assert self.l > 15
        assert self.l > self.front.l + 4
        assert self.h > self.back.h + 4
        assert self.h > self.front.h + 6

    def take_green(self):
        self.grn.decrement()

    def take_red(self):
        self.red.decrement()

    def add_green(self):
        self.grn.increment()

    def add_red(self):
        self.red.increment()

    def render_back(self):
        ballooned = self.back.balloon_to(self.h - 2, self.l - 2)
        bordered = ballooned.add_border(False)
        return bordered 

    def render_name(self):
        tag = f'r{self.idx}'
        assert isinstance(tag, str)
        assert len(tag) <= 4
        mid_pad = self.l - len(self.name) - 4 - len(tag)
        return Render.from_string('_' + self.name + '_' * mid_pad + tag + '_').add_border(True)

    def render_effect(self):
        right_pad = self.l - len(self.effect) - 3
        return Render.from_string('_' + self.effect + '_' * right_pad).add_border(True)

    def render_pic(self):
        return self.front.balloon_to(self.h - 4, self.l - 2).add_border(False)

    def render_front(self):
        name   = self.render_name()
        effect = self.render_effect()
        pic    = self.render_pic()
        red    = self.red.render()
        grn    = self.grn.render()
        return name.stack_above(effect, True
                  ).stack_above(pic, True
                  ).insert_from(red, self.h - 1, 1
                  ).insert_from(grn, self.h - 1, self.l - 7)

class AreaCard:
    def __init__(self):
        self.subareas = list()

    def add_subarea(self, subarea):
        self.subareas.append(subarea)

    def render_front(self):
        target = self.subareas[0].render_front()
        if len(self.subareas) > 1:
            target = target.stack_above(self.subareas[1].render_front(), False)
        return target

    def render_back(self):
        return self.subareas[0].render_back()
