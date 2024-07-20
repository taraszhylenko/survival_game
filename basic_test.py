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
        board.animal_dict[1].render(board.trait_dict).print()
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
    
    def test_boolean(self):
        a = True
        b = True
        self.assertEqual(a, b)
