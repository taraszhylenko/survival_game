import pandas as pd
import numpy  as np
import random

from engine.area.card    import SubAreaCard
from engine.deck import Deck
from engine.render import Render
from engine.enum import StartIndex, EndIndex

class AreaDeckMaker:
    @staticmethod
    def from_csv(csv_file):
        deck_df = pd.read_csv(csv_file).fillna('').astype({'name1':     str,
                                                          'effect1':   str,
                                                          'back_txt1': str,
                                                          'front_txt1': str,
                                                          'name2':     str,
                                                          'effect2':   str,
                                                          'back_txt2': str,
                                                          'front_txt2': str,
                                                          'quantity':  int})
        l = 0
        h = 0
        for _, row in deck_df.iterrows():
            name1 = row.name1
            name2 = row.name2
            effect1 = row.effect1
            effect2 = row.effect2
            back1 = Render.from_txt(row.back_txt1)
            back2 = Render.from_txt(row.back_txt2)
            front1 = Render.from_txt(row.front_txt1)
            front2 = Render.from_txt(row.front_txt2)
            l = max([l, len(name1) + 3, len(effect1) + 3,
                        len(name2) + 3, len(effect2) + 3,
                        back1.l + 2,    front1.l + 2,
                        back2.l + 2,    front2.l + 2,
                        13])
            h = max([h, back1.h + 2, front1.h + 4,
                        back2.h + 2, front2.h + 4])


        idx = StartIndex.AREA 
        subarea_dict = dict()
        area_deck    = Deck()
        area_discard = Deck()
        for _, row in deck_df.iterrows():
            for _ in range(row.quantity):
                name1 = row.name1
                name2 = row.name2
                effect1 = row.effect1
                effect2 = row.effect2
                back1 = Render.from_txt(row.back_txt1)
                back2 = Render.from_txt(row.back_txt2)
                front1 = Render.from_txt(row.front_txt1)
                front2 = Render.from_txt(row.front_txt2)
                s1 = SubAreaCard([name1, effect1],
                                 [back1, front1],
                                 h, l, str(idx))
                a = Area.create(idx) 
                subarea_dict[idx] = s1
                idx += 1
                assert StartIndex.AREA <= idx <= EndIndex.AREA
                if name2 != '':
                    s2 = SubAreaCard([name2, effect2],
                                     [back2, front2],
                                     h, l, str(idx))
                    subarea_dict[idx] = s2
                    a = Area.add_subarea(idx)
                    idx += 1
                    assert StartIndex.AREA <= idx <= EndIndex.AREA
                Deck.add(a)
        placeholder = SubAreaCard(['empty', 'empty'], [back1, front1], h, l, str(idx))
        subarea_dict[idx] = placeholder
        placeholder_area = Area.create(idx)
        area_discard.add(placeholder)
        return ad

    def add_card_spec(self, subareas):
        subareas_rendered = list()
        for name, effect, red, green, back_txt, front_txt in subareas:
            back = Render.from_txt(back_txt)
            front = Render.from_txt(front_txt)
            subareas_rendered.append((name, effect, int(red), int(green), back, front))
            self.l = max([self.l, len(name) + 10, len(effect) + 5, back.l + 5, front.l + 5, 12])
            self.h = max([self.h, back.h + 5, front.h + 7])
        self.card_tuples.append(subareas_rendered)

    def create_cards(self):
        idx = 0
        for subareas_rendered in self.card_tuples:
            ac = AreaCard()
            for name, effect, red, green, back, front in subareas_rendered:
                ac.add_subarea(SubArea(name, effect, red, green, back, front, self.h, self.l, idx))
                idx += 1
            self.add_card(ac)
