from engine.render import Render

class EvolutionCard:
    def __init__(self, main, short, back, front, h, l):
        self.main  = main
        self.short = short
        self.back  = back
        self.front = front
        self.h = h
        self.l = l
        self.checks()
   
    def checks(self):
        assert isinstance(self.back,  Render)
        assert isinstance(self.front, Render)
        assert self.l > len(self.main) + 9
        assert self.l > len(self.short) + 9
        assert self.l > self.back.l + 4 
        assert self.l > self.front.l + 4 
        assert self.h > self.back.h + 4 
        assert self.h > self.front.h + 8 

    def render_back(self):
        return self.back.balloon_to(self.h - 2, self.l - 2).add_border(False)

    def render_main(self, tag):
        assert isinstance(tag, str)
        assert len(tag) <= 4
        mid_pad = self.l - len(self.main) - 4 - len(tag)
        return Render.from_string('_' + self.main + '_' * mid_pad + tag + '_').add_border()  

    def render_mid(self):
        pass

    def render_short(self):
        pass
