from engine.render import Render

class EvolutionCard:
    def __init__(self, main, short, back, front, h, l, reqs):
        self.main  = main
        self.short = short
        self.back  = back
        self.front = front
        self.h = h
        self.l = l
        self.reqs = reqs
        self.checks()
   
    def checks(self):
        assert isinstance(self.back,  Render)
        assert isinstance(self.front, Render)
        assert self.l > len(self.main) + 9
        assert self.l > len(self.short) + 9
        assert self.l > self.back.l + 4 
        assert self.l > self.front.l + 4 
        assert self.h > self.back.h + 4 
        assert self.h > self.front.h + 6 
        assert isinstance(self.reqs,  dict)

    def render_back(self, tag):
        assert isinstance(tag, str)
        assert len(tag) <= 4
        ballooned = self.back.balloon_to(self.h - 2, self.l - 2)
        bordered = ballooned.add_border(False)
        render_tag = Render.from_string(tag)
        inserted = bordered.insert_from(render_tag, bordered.h-1, bordered.l - 2 - len(tag))
        return inserted 

    def render_front(self):
        main  = self.render_main('')
        pic   = self.render_pic()
        short = self.render_short('')
        return main.stack_above(pic, True).stack_above(short, True)

    def render_main(self, tag):
        assert isinstance(tag, str)
        assert len(tag) <= 4
        mid_pad = self.l - len(self.main) - 4 - len(tag)
        return Render.from_string('_' + self.main + '_' * mid_pad + tag + '_').add_border(True) 

    def render_pic(self):
        return self.front.balloon_to(self.h - 4, self.l - 2).add_border(False)

    def render_short(self, tag):
        assert isinstance(tag, str)
        assert len(tag) <= 4
        mid_pad = self.l - len(self.short) - 4 - len(tag)
        return Render.from_string('_' + self.short + '_' * mid_pad + tag + '_').add_border(True) 

    def req(self, side):
        assert side in {'main', 'short'}
        return self.reqs[side]
