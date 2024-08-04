import pandas as pd
import unittest

class Testing(unittest.TestCase):
    def test_game1(self):
        import random
        random.seed(31)
        import numpy as np
        np.random.seed(31)
        from engine.game import Game
        from engine.enum import TraitType as tt, ItemType as it
        gg = Game('asset/deck/evolution/base.txt',
                  'asset/deck/area/base.txt',
                  2)
        gg.draw(0)
        gg.draw(0)
        gg.draw(0)
        gg.draw(0)
        gg.draw(1)
        gg.draw(1)
        gg.draw(1)
        gg.draw(1)
        t1  = gg.cast_animal(0, 14)
        t2  = gg.cast_trait(1, 17, tt.SHORT, [14]) 
        t3  = gg.cast_animal(0, 60)
        t4  = gg.cast_trait(0, 50, tt.SHORT, [14, 60]) 
        t5  = gg.render().arr
        t6  = gg.cast_animal(1, 18)
        t7  = gg.cast_trait(1, 87, tt.MAIN, [18])
        t8  = gg.place_area()
        t9  = gg.render().arr
        t10 = gg.place_area()
        t11 = gg.render().arr
        t12 = gg.cast_trait(0, 50, tt.SHORT, [60])
        t12 = gg.swap_animals(0, 14, 50)
        t13 = gg.swap_animals(0, 14, 60)
        t14 = gg.render().arr
        t15 = gg.cast_trait(1, 5, tt.SHORT, [18])
        t16 = gg.take_item(1, 18, it.RED, 220)
        t17 = gg.take_item(1, 18, it.RED, 221)
        t18 = gg.take_item(1, 18, it.RED, 221)
        t19 = gg.take_item(1, 18, it.RED, 216)
        t20 = gg.take_item(1, 18, it.RED, 216)
        t21 = gg.render().arr
        t22 = gg.run_extinction()
        t23 = gg.render().arr
        t24 = gg.run_extinction()
        t25 = gg.render().arr
        self.assertTrue(t1 == t3 == t6 == t7 == t8 == t10 == t13 == t15 == t17 == t19 == t22 == t24 == 'ok')
        self.assertTrue(t2 == 'Transition infeasible: holds=True; appropriate_targets=True; animals_in_herds=True; same_herd=True; detrimental_check=False; can_add_trait=True')
        self.assertTrue(t4 == 'Transition infeasible: holds=True; appropriate_targets=False; animals_in_herds=True; same_herd=True; detrimental_check=True; can_add_trait=True')
        self.assertTrue(t12 == 'Transition infeasible: controls1=True; controls2=False')
        self.assertTrue(t16 == 'Transition infeasible: player_owns_animal=True area_has_item=True area_accessible=False can_eat=True can_hide=True')
        self.assertTrue(t18 == 'Transition infeasible: player_owns_animal=True area_has_item=False area_accessible=True can_eat=True can_hide=True')
        self.assertTrue(t20 == 'Transition infeasible: player_owns_animal=True area_has_item=True area_accessible=True can_eat=False can_hide=True')
        e1 = pd.read_csv('asset/test/10/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/10/2.csv').to_numpy()
        e3 = pd.read_csv('asset/test/10/3.csv').to_numpy()
        e4 = pd.read_csv('asset/test/10/4.csv').to_numpy()
        e5 = pd.read_csv('asset/test/10/5.csv').to_numpy()
        e6 = pd.read_csv('asset/test/10/6.csv').to_numpy()
        e7 = pd.read_csv('asset/test/10/7.csv').to_numpy()
        self.assertTrue((e1 == t5 ).all())
        self.assertTrue((e2 == t9 ).all())
        self.assertTrue((e3 == t11).all())
        self.assertTrue((e4 == t14).all())
        self.assertTrue((e5 == t21).all())
        self.assertTrue((e6 == t23).all())
        self.assertTrue((e7 == t25).all())

    def test_habitat(self):
        import random
        random.seed(31)
        import numpy as np
        np.random.seed(31)
        from engine.render import Render
        from engine.area.card import SubAreaCard, Area
        from engine.area.deck_maker import AreaDeckMaker
        from engine.area.habitat import Habitat
        sadict, adeck, adisc, _, _ = AreaDeckMaker.from_csv('asset/deck/area/base.txt')
        adeck.shuffle()
        a1 = adeck.draw()
        a2 = adeck.draw()
        a3 = adeck.draw()
        h = Habitat()
        h.place(a1)
        h.place(a2)
        t1 = h.render(sadict).arr
        h.place(a3)
        t2 = h.render(sadict).arr
        h.pop()
        t3 = h.render(sadict).arr
        e1 = pd.read_csv('asset/test/1/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/1/2.csv').to_numpy()
        e3 = pd.read_csv('asset/test/1/3.csv').to_numpy()
        self.assertTrue((t1 == e1).all())
        self.assertTrue((t2 == e2).all())
        self.assertTrue((t3 == e3).all())

    def test_area_deck(self):
        import random
        random.seed(20)
        import numpy as np
        np.random.seed(20)
        from engine.render import Render
        from engine.area.card import SubAreaCard, Area
        from engine.area.deck_maker import AreaDeckMaker
        sadict, adeck, adisc, _, _ = AreaDeckMaker.from_csv('asset/deck/area/base.txt')
        adeck.shuffle()
        aa1 = adeck.draw()
        aa2 = adeck.draw()
        aa3 = adeck.draw()
        t1 = Area.render_front(aa1, sadict).arr
        t2 = Area.render_front(aa2, sadict).arr
        t3 = Area.render_front(aa3, sadict).arr
        t4 = adeck.render(sadict).arr
        t5 = adisc.render(sadict).arr
        e1 = pd.read_csv('asset/test/2/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/2/2.csv').to_numpy()
        e3 = pd.read_csv('asset/test/2/3.csv').to_numpy()
        e4 = pd.read_csv('asset/test/2/4.csv').to_numpy()
        e5 = pd.read_csv('asset/test/2/5.csv').to_numpy()
        self.assertTrue((t1 == e1).all())
        self.assertTrue((t2 == e2).all())
        self.assertTrue((t3 == e3).all())
        self.assertTrue((t4 == e4).all())
        self.assertTrue((t5 == e5).all())

    def test_hand(self):
        import random
        random.seed(20)
        import numpy as np
        np.random.seed(20)
        from engine.evolution.deck_maker import EvolutionDeckMaker
        from engine.enum import TraitType as tt
        evolution_dict, evolution_deck, evolution_discard, _, _ = EvolutionDeckMaker.from_csv('asset/deck/evolution/base.txt')
        evolution_deck.shuffle()
        from engine.evolution.hand import Hand
        hh = Hand()
        cc = [evolution_deck.draw() for _ in range(10)]
        hh.add(cc[0])
        hh.add(cc[1])
        hh.add(cc[2])
        hh.add(cc[3])
        hh.add(cc[4])
        hh.add(cc[5])
        t1 = hh.render(evolution_dict).arr
        hh.discard(cc[4])
        hh.discard(cc[2])
        hh.discard(cc[0])
        t2 = hh.render(evolution_dict).arr
        e1 = pd.read_csv('asset/test/9/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/9/2.csv').to_numpy()
        self.assertTrue((t1 == e1).all())
        self.assertTrue((t2 == e2).all())

    def test_herd(self):
        import random
        random.seed(20)
        import numpy as np
        np.random.seed(20)
        from engine.evolution.deck_maker import EvolutionDeckMaker
        from engine.enum import TraitType as tt
        evolution_dict, evolution_deck, evolution_discard, _, _ = EvolutionDeckMaker.from_csv('asset/deck/evolution/base.txt')
        evolution_deck.shuffle()
        from engine.evolution.herd import Herd
        hh = Herd()
        cc = [evolution_deck.draw() for _ in range(10)]
        hh.cast_animal(cc[0])
        hh.cast_animal(cc[1])
        hh.cast_animal(cc[2])
        hh.cast_trait(cc[3], tt.MAIN,  cc[0])
        hh.cast_trait(cc[4], tt.SHORT, cc[1])
        hh.cast_trait(cc[5], tt.MAIN,  cc[2])
        hh.cast_trait(cc[6], tt.SHORT, cc[2])
        hh.cast_trait(cc[7], tt.MAIN,  cc[1])
        t1 = hh.render(evolution_dict).arr
        hh.swap_animals(cc[0], cc[1])
        t2 = hh.render(evolution_dict).arr
        e1 = pd.read_csv('asset/test/8/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/8/2.csv').to_numpy()
        self.assertTrue((t1 == e1).all())
        self.assertTrue((t2 == e2).all())

    def test_evolution_deckmaker(self):
        import random
        random.seed(20)
        import numpy as np
        np.random.seed(20)
        from engine.evolution.deck_maker import EvolutionDeckMaker
        evolution_dict, evolution_deck, evolution_discard, _, _ = EvolutionDeckMaker.from_csv('asset/deck/evolution/base.txt')
        c1  = evolution_dict[1]
        c2 = evolution_dict[35]
        e1 = pd.read_csv('asset/test/7/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/7/2.csv').to_numpy()
        e3 = pd.read_csv('asset/test/7/3.csv').to_numpy()
        self.assertTrue((c1.render_front(True).arr == e1).all())
        self.assertTrue((c2.render_front(True).arr == e2).all())
        self.assertTrue((evolution_deck.render(evolution_dict).arr == e3).all())
        self.assertTrue((evolution_discard.render(evolution_dict).arr == e3).all())

    def test_evolution_deck(self):
        from engine.render import Render
        from engine.evolution.card import EvolutionCard
        from engine.deck import Deck
        from engine.enum import DeckType
        import random
        random.seed(20)
        h = 10
        l = 18
        moose = Render.from_txt('asset/card/evolution/back/moose1.txt').balloon_to(h-2, l-2).add_border(False)
        blank = Render.blank(1, 1).balloon_to(h-4, l-2).add_border(False)
        c0 = EvolutionCard(['poisonous', 'swimming'],
                [moose, blank], h, l, '0')
        c1 = EvolutionCard(['flying', 'carnivorous'], 
                [moose, blank], h, l, '1')
        c2 = EvolutionCard(['piracy', 'fat_tissue'],
                [moose, blank], h, l, '2')
        evolution_dict = {0: c0, 1: c1, 2: c2}
        ed = Deck(DeckType.EVOLUTION)
        ed.add(0)
        ed.add(1)
        ed.add(2)
        ed.shuffle()

        self.assertTrue(ed.things == [1, 0, 2])
        e1 = pd.read_csv('asset/test/6/1.csv').to_numpy()
        self.assertTrue((ed.render(evolution_dict).arr == e1).all())
        e2 = pd.read_csv('asset/test/6/2.csv').to_numpy()
        self.assertTrue((evolution_dict[ed.draw()].render_front(True).arr == e2).all())

    def test_animal(self):
        from engine.render import Render
        from engine.evolution.card import EvolutionCard
        from engine.evolution.animal import Animal
        from engine.enum import TraitType as tt
        h = 10
        l = 18
        moose = Render.from_txt('asset/card/evolution/back/moose1.txt').balloon_to(h-2, l-2).add_border(False)
        blank = Render.blank(1, 1).balloon_to(h-4, l-2).add_border(False)
        c0 = EvolutionCard(['poisonous', 'swimming'],
                [moose, blank], h, l, '0')
        c1 = EvolutionCard(['flying', 'carnivorous'], 
                [moose, blank], h, l, '1')
        c2 = EvolutionCard(['piracy', 'fat_tissue'],
                [moose, blank], h, l, '2')

        a1 = [0]
        # a1 = Animal(0)
        a1 = Animal.add_trait(a1, 1, tt.MAIN)
        a1 = Animal.add_trait(a1, 2, tt.SHORT)

        e1 = pd.read_csv('asset/test/5/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/5/2.csv').to_numpy()

        self.assertTrue((e1 == Animal.render(a1, {0: c0, 1: c1, 2: c2}).arr).all())
        self.assertTrue((e2 == Animal.render(a1, {0: c0, 1: c2, 2: c1}).arr).all())

    def test_evolution_card(self):
        from engine.enum import TraitType as tt
        from engine.render import Render
        from engine.evolution.card import EvolutionCard
        h = 10
        l = 18
        moose = Render.from_txt('asset/card/evolution/back/moose1.txt').balloon_to(h-2, l-2).add_border(False)
        blank = Render.blank(1, 1).balloon_to(h-4, l-2).add_border(False)
        c1 = EvolutionCard(['piracy', 'fat_tissue'],
                [moose, blank], h, l, '0')
        e1 = pd.read_csv('asset/test/4/front.csv').to_numpy()
        e2 = pd.read_csv('asset/test/4/back.csv').to_numpy()
        e3 = pd.read_csv('asset/test/4/main.csv').to_numpy()
        e4 = pd.read_csv('asset/test/4/short.csv').to_numpy()

        self.assertTrue((c1.render_front(True).arr == e1           ).all())
        self.assertTrue((c1.render_back(True).arr  == e2           ).all())
        self.assertTrue((c1.render_trait(tt.MAIN,  False).arr == e3).all())
        self.assertTrue((c1.render_trait(tt.SHORT, True).arr  == e4).all())

    def test_area_subarea(self):
        import random
        random.seed(20)
        import numpy as np
        np.random.seed(20)
        from engine.render import Render
        from engine.area.card import SubAreaCard, Area
        from engine.enum import AreaTextType as at
        h = 12
        l = 22                                     
        tree     = Render.from_txt('asset/card/area/back/tree1.txt').balloon_to(h-2, l-2).add_border(False)
        daffodil = Render.from_txt('asset/card/area/back/daffodil1.txt').balloon_to(h-4, l-2).add_border(False)
        s1 = SubAreaCard(['glaciers', ''],          [tree, daffodil], h, l, '101')
        s2 = SubAreaCard(['tundra',   'no_traits'], [tree, daffodil], h, l, '102')
        t1 = s1.render_back(True).arr
        t2 = s1.render_front(True).arr
        subareadict = {101: s1, 102: s2}
        a1 = Area.create(101)
        a1 = Area.add_subarea(a1, 102)
        t3 = Area.render_front(a1, subareadict).arr
        t4 = Area.render_back(a1, subareadict).arr
        e1 = pd.read_csv('asset/test/3/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/3/2.csv').to_numpy()
        e3 = pd.read_csv('asset/test/3/3.csv').to_numpy()
        e4 = pd.read_csv('asset/test/3/4.csv').to_numpy()
        self.assertTrue((e1 == t1).all())
        self.assertTrue((e2 == t2).all())
        self.assertTrue((e3 == t3).all())
        self.assertTrue((e4 == t4).all())

