from engine.enum import Side as sd
from engine.enum import AreaTextType as at
from engine.render import Render

class SubAreaCard:
    def __init__(self, texts, pics, h, l, tag):
        self.texts = texts
        self.pics = pics
        self.h = h
        self.l = l
        self.tag = tag
        self.checks()

    def checks(self):
        assert isinstance(self.pics[0], Render)
        assert isinstance(self.pics[1], Render)
        assert self.l >= len(self.texts[0]) + 3
        assert self.l >= len(self.texts[1]) + 3
        assert isinstance(self.tag, str)
        assert isinstance(self.texts[0], str)
        assert isinstance(self.texts[1], str)

    def render_back(self, with_tag):
        return self.render_pic(sd.FACEDOWN, with_tag)

    def render_front(self, with_tag):
        name   = self.render_text(at.NAME)
        effect = self.render_text(at.EFFECT)
        pic    = self.render_pic(sd.FACEUP, with_tag)
        return name.stack_above(effect, True).stack_above(pic, True)
  
    def render_pic(self, side, with_tag):
        return self.pics[side].insert_tag_br(self.tag if with_tag else '')

    def render_text(self, text_type):
        text = self.texts[text_type]
        rendered = Render.from_string(text)
        for _ in range(self.l - 2 - len(text)):
            rendered = rendered.pad('right', '_')
        return rendered.add_border(True) 

class Area:
    @staticmethod
    def create(card):
        return [card]

    @staticmethod
    def add_subarea(card_list, card):
        return card_list + [card]

    @staticmethod
    def render_front(card_list, card_dict):
        assert len(card_list) > 0
        target = card_dict[card_list[0]].render_front(True)
        for c in card_list[1:]:
            target = target.stack_above(card_dict[c].render_front(True), True)
        return target

    @staticmethod
    def render_back(card_list, card_dict):
        assert len(card_list) > 0
        target = card_dict[card_list[0]].render_back(False)
        return target
