from engine.render import Render
from engine.enum import CardOrientation as co
from engine.enum import TraitType       as tt

class EvolutionCard:
    def __init__(self, traits, back, front, h, l, tag):
        self.traits = traits
        self.pics   = [back.balloon_to( h - 2, l - 2).add_border(False),
                       front.balloon_to(h - 4, l - 2).add_border(False)]
        self.h   = h
        self.l   = l
        self.tag = tag
        self.checks()
   
    def checks(self):
        for pic in self.pics:
            assert isinstance(pic, Render)
        for trait in self.traits:
            assert self.l > len(trait) + 9
        back  = self.pics[co.FACEDOWN]
        front = self.pics[co.FACEUP]
        assert isinstance(self.tag, str)
        assert len(self.tag) < 3

    def render_back(self, with_tag):
        return self.render_pic(co.FACEDOWN, with_tag)

    def render_front(self, with_tag):
        main  = self.render_trait(tt.MAIN,  False)
        pic   = self.render_pic(co.FACEUP, with_tag)
        short = self.render_trait(tt.SHORT, False)
        return main.stack_above(pic, True).stack_above(short, True)
    
    def render_pic(self, card_orientation, with_tag):
        return self.pics[card_orientation].insert_tag_br(self.tag if with_tag else '')

    def render_trait(self, trait_type, with_tag):
        trait = self.traits[trait_type] 
        rendered = Render.from_string(trait)
        for _ in range(self.l - 2 - len(trait)):
            rendered = rendered.pad('right', '_')
        bordered = rendered.add_border(True)
        return bordered.insert_tag_br(self.tag if with_tag else '') 
