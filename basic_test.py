import pandas as pd
import unittest

class Testing(unittest.TestCase):
    def test_evolution_deck(self):
        from engine.render import Render
        from engine.evolution.card import EvolutionCard
        from engine.deck import Deck
        import random
        random.seed(20)
        moose = Render.from_txt('asset/card/evolution/back/moose1.txt')
        blank = Render.blank(1, 1)
        c0 = EvolutionCard(['poisonous', 'swimming'],
                moose, blank, 10, 18, '0')
        c1 = EvolutionCard(['flying', 'carnivorous'], 
                moose, blank, 10, 18, '1')
        c2 = EvolutionCard(['piracy', 'fat_tissue'],
                moose, blank, 10, 18, '2')
        evolution_dict = {0: c0, 1: c1, 2: c2}
        ed = Deck()
        ed.add_card(0)
        ed.add_card(1)
        ed.add_card(2)
        ed.shuffle()

        self.assertTrue(ed.cards == [1, 0, 2])
        e1 = pd.read_csv('asset/test/6/1.csv').to_numpy()
        self.assertTrue((ed.render(evolution_dict).arr == e1).all())
        e2 = pd.read_csv('asset/test/6/2.csv').to_numpy()
        self.assertTrue((evolution_dict[ed.draw()].render_front(True).arr == e2).all())

    def test_animal(self):
        from engine.render import Render
        from engine.evolution.card import EvolutionCard
        from engine.evolution.playable.animal import Animal
        from engine.enum import TraitType as tt
        moose = Render.from_txt('asset/card/evolution/back/moose1.txt')
        blank = Render.blank(1, 1)
        c0 = EvolutionCard(['poisonous', 'swimming'],
                moose, blank, 10, 18, '0')
        c1 = EvolutionCard(['flying', 'carnivorous'], 
                moose, blank, 10, 18, '1')
        c2 = EvolutionCard(['piracy', 'fat_tissue'],
                moose, blank, 10, 18, '2')
        
        a1 = Animal(0)
        a1.add_trait(1, tt.MAIN)
        a1.add_trait(2, tt.SHORT)

        e1 = pd.read_csv('asset/test/5/1.csv').to_numpy()
        e2 = pd.read_csv('asset/test/5/2.csv').to_numpy()

        self.assertTrue((e1 == a1.render({0: c0, 1: c1, 2: c2}).arr).all())
        self.assertTrue((e2 == a1.render({0: c0, 1: c2, 2: c1}).arr).all())

    def test_evolution_card(self):
        from engine.enum import TraitType as tt
        from engine.render import Render
        from engine.evolution.card import EvolutionCard
        c1 = EvolutionCard(['piracy', 'fat_tissue'], 
                           Render.from_txt('asset/card/evolution/back/moose1.txt'),
                           Render.blank(1, 1), 10, 17, '0')
        e1 = pd.read_csv('asset/test/4/front.csv').to_numpy()
        e2 = pd.read_csv('asset/test/4/back.csv').to_numpy()
        e3 = pd.read_csv('asset/test/4/main.csv').to_numpy()
        e4 = pd.read_csv('asset/test/4/short.csv').to_numpy()
        
        self.assertTrue((c1.render_front(True).arr == e1           ).all())
        self.assertTrue((c1.render_back(True).arr  == e2           ).all())
        self.assertTrue((c1.render_trait(tt.MAIN,  False).arr == e3).all())
        self.assertTrue((c1.render_trait(tt.SHORT, True).arr  == e4).all())


    def test_big_board(self):
        import random
        random.seed(20)
        from engine.render import Render
        from engine.evolution.card import EvolutionCard
        from engine.evolution.deck import EvolutionDeck
        from engine.evolution.playable.trait import Trait
        from engine.evolution.playable.animal import Animal
        from engine.board import Board
        edeck = EvolutionDeck.from_csv('asset/deck/evolution/base.txt')
        ediscard = EvolutionDeck()
        ediscard.h = edeck.h
        ediscard.l = edeck.l
        board = Board(edeck, ediscard, None, None)
        board.cast_animal(board.evolution_deck.draw(), 0)
        board.cast_trait(board.evolution_deck.draw(), 'main', 0)
        board.cast_trait(board.evolution_deck.draw(), 'short', 0)
        board.cast_trait(board.evolution_deck.draw(), 'main', 0)
        board.cast_trait(board.evolution_deck.draw(), 'short', 0)
        board.cast_trait(board.evolution_deck.draw(), 'main', 0)
        board.cast_trait(board.evolution_deck.draw(), 'short', 0)
        board.cast_animal(board.evolution_deck.draw(), 0)
        board.cast_trait(board.evolution_deck.draw(), 'main', 1)
        board.cast_trait(board.evolution_deck.draw(), 'short', 1)
        board.cast_trait(board.evolution_deck.draw(), 'main', 1)
        board.cast_trait(board.evolution_deck.draw(), 'short', 1)
        board.cast_trait(board.evolution_deck.draw(), 'main', 1)
        board.cast_trait(board.evolution_deck.draw(), 'short', 1)
        board.discard_trait(9)
        board.discard_trait(8)
        board.discard_trait(7)
        board.cast_animal(board.evolution_deck.draw(), 1)
        board.cast_trait(board.evolution_deck.draw(), 'main',  2)
        board.cast_trait(board.evolution_deck.draw(), 'short', 0)
        board.cast_trait(board.evolution_deck.draw(), 'main',  0)
        board.cast_trait(board.evolution_deck.draw(), 'short', 0)
        board.cast_trait(board.evolution_deck.draw(), 'main',  2)
        board.cast_trait(board.evolution_deck.draw(), 'short', 2)
        board.cast_animal(board.evolution_deck.draw(), 1)
        board.cast_trait(board.evolution_deck.draw(), 'main',  3)
        board.cast_trait(board.evolution_deck.draw(), 'short', 3)
        board.cast_trait(board.evolution_deck.draw(), 'main',  3)
        board.cast_trait(board.evolution_deck.draw(), 'short', 3)
        board.cast_trait(board.evolution_deck.draw(), 'main',  3)
        board.cast_trait(board.evolution_deck.draw(), 'short', 1)
        expected = pd.read_csv('asset/test/1/board_render.csv')
        self.assertTrue((board.render().arr == expected.to_numpy()).all())
    
    def test_area_card(self):
        from engine.area.card import SubArea, AreaCard
        from engine.render import Render
        s1 = SubArea('glaciers', 'without_traits', 1, 0, Render.from_string('*'),       Render.from_string('#'), 10, 20, 0)
        s2 = SubArea('tundra',   '', 1, 0,           Render.from_string('*'),       Render.from_string('#'), 10, 20, 1)
        s1.add_green()
        s1.add_green()
        c1 = AreaCard()
        c1.add_subarea(s1)
        c1.add_subarea(s2)
        c1.render_front()
        expected = pd.read_csv('asset/test/2/areacard_render.csv')
        self.assertTrue((c1.render_front().arr == expected.to_numpy()).all())

    def test_area_deck(self):
        import random
        random.seed(20)
        from engine.area.deck import AreaDeck
        ad = AreaDeck.from_csv('asset/deck/area/base.txt')
        
        expf1 = pd.read_csv('asset/test/3/f1.csv').to_numpy()
        expb1 = pd.read_csv('asset/test/3/b1.csv').to_numpy()
        c1 = ad.draw()
        self.assertTrue((c1.render_front().arr == expf1).all())
        self.assertTrue((c1.render_back().arr  == expb1).all())
        
        expf2 = pd.read_csv('asset/test/3/f2.csv').to_numpy()
        expb2 = pd.read_csv('asset/test/3/b2.csv').to_numpy()
        c2 = ad.draw()
        self.assertTrue((c2.render_front().arr == expf2).all())
        self.assertTrue((c2.render_back().arr  == expb2).all())
        
        expf3 = pd.read_csv('asset/test/3/f3.csv').to_numpy()
        expb3 = pd.read_csv('asset/test/3/b3.csv').to_numpy()
        c3 = ad.draw()
        self.assertTrue((c3.render_front().arr == expf3).all())
        self.assertTrue((c3.render_back().arr  == expb3).all())
        
        expf4 = pd.read_csv('asset/test/3/f4.csv').to_numpy()
        expb4 = pd.read_csv('asset/test/3/b4.csv').to_numpy()
        c4 = ad.draw()
        self.assertTrue((c4.render_front().arr == expf4).all())
        self.assertTrue((c4.render_back().arr  == expb4).all())
        
        exp5 = pd.read_csv('asset/test/3/5.csv').to_numpy()
        exp6 = pd.read_csv('asset/test/3/6.csv').to_numpy()
        self.assertTrue((ad.render().arr           == exp5).all())
        self.assertTrue((ad.render_last_card().arr == exp6).all())
