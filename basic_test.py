import pandas as pd
import unittest

class Testing(unittest.TestCase):
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
    
    def test_area(self):
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

