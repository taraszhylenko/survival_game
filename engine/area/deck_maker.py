import pandas as pd
import numpy  as np
import random

from engine.area.card    import SubAreaCard, Area
from engine.deck import Deck
from engine.render import Render
from engine.enum import StartIndex, EndIndex, DeckType

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
            front1 = Render.from_txt(row.front_txt1)
            l = max([l, len(name1) + 3, len(effect1) + 3,
                        back1.l + 2,    front1.l + 2,
                        13])
            h = max([h, back1.h + 2, front1.h + 4])
            if name2 != '': 
                back2 = Render.from_txt(row.back_txt2)
                front2 = Render.from_txt(row.front_txt2)
                l = max([l, len(name2) + 3, len(effect2) + 3,
                            back2.l + 2,    front2.l + 2,
                            13])
                h = max([h, back2.h + 2, front2.h + 4])


        idx = int(StartIndex.AREA) 
        subarea_dict = dict()
        area_deck    = Deck(DeckType.AREA)
        area_discard = Deck(DeckType.AREA)
        for _, row in deck_df.iterrows():
            for _ in range(row.quantity):
                name1 = row.name1
                name2 = row.name2
                effect1 = row.effect1
                back1 = Render.from_txt(row.back_txt1).balloon_to(h - 2, l - 2).add_border(False)
                front1 = Render.from_txt(row.front_txt1).balloon_to(h - 4, l - 2).add_border(False)
                s1 = SubAreaCard([name1, effect1],
                                 [back1, front1],
                                 h, l, str(idx))
                a = Area.create(idx) 
                subarea_dict[idx] = s1
                idx += 1
                assert StartIndex.AREA <= idx <= EndIndex.AREA
                if name2 != '':
                    front2 = Render.from_txt(row.front_txt2).balloon_to(h - 4, l - 2).add_border(False)
                    back2 = Render.from_txt(row.back_txt2).balloon_to(h - 2, l - 2).add_border(False)
                    effect2 = row.effect2
                    s2 = SubAreaCard([name2, effect2],
                                     [back2, front2],
                                     h, l, str(idx))
                    subarea_dict[idx] = s2
                    a = Area.add_subarea(a, idx)
                    idx += 1
                    assert StartIndex.AREA <= idx <= EndIndex.AREA
                area_deck.add(a)
        placeholder = SubAreaCard(['empty', 'empty'], [back1, front1], h, l, str(idx))
        subarea_dict[idx] = placeholder
        placeholder_area = Area.create(idx)
        area_discard.add(placeholder_area)
        return subarea_dict, area_deck, area_discard, h, l
