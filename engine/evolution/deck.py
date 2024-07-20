import random

from engine.evolution.card import EvolutionCard
from engine.render import Render

class EvolutionDeck:
    def __init__(self):
        self.cards = list()
        self.h = 0
        self.l = 0
        self.card_tuples = list()
        self.cards = list()

    def add_card_spec(self, main, short, back_txt, front_txt):
        back = Render.from_txt(back_txt)
        front = Render.from_txt(front_txt)
        self.card_tuples.append((main, short, back, front))
        self.l = max([self.l, back.l + 5, len(short) + 10, len(main) + 10, front.l + 5])
        self.h = max([self.h, back.h + 5, front.h + 7])

    def create_cards(self):
        for main, short, back, front in self.card_tuples:
            self.cards.append(EvolutionCard(main, short, back, front, self.h, self.l))


    def shuffle(self):
        random.shuffle(self.cards)
