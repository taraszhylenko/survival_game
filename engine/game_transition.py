def find_animal_herd(game, card):
    idx = -1
    for i in range(game.num_players):
        if game.herds[i].find_animal_index(card) != -1:
            idx = i
    return idx

def find_trait_herd(game, card):
    idx = -1
    for i in range(game.num_players):
        if game.herds[i].find_trait_index(card) != -1:
            idx = i
    return idx

class CastAnimal:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        self.player = args['player']
        self.card = args['card']
    
    def feasible(self, game):
        has_card = game.hands[self.player].find_index(self.card) != -1
        if has_card:
            return True, 'ok'
        else:
            return False, f"Player {self.player} doesn't have card {self.card}"

    def apply(self, game):
        game.hands[self.player].discard(self.card)
        game.herds[self.player].cast_animal(self.card)

class CastTrait:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        assert 'trait_type' in args
        assert 'target_cards' in args
        self.player       = args['player']
        self.card         = args['card']
        self.trait_type   = args['trait_type']
        self.target_cards = args['target_cards']

    def feasible(self, game):
        has_card = game.hands[self.player].find_index(self.card) != -1
        one_or_two_targets = 0 < len(self.target_cards) < 3
        animals_in_herds = all([find_animal_herd(game, tc) != -1 for tc in self.target_cards])
        if has_card and one_or_two_targets and animals_in_herds:
            return True, 'ok'
        else:
            return False, f"{has_card=}; {one_or_two_targets=}; {animals_in_herds=}"

    def apply(self, game):
        game.hands[self.player].discard(self.card)
        for tc in self.target_cards:
            tp = find_animal_herd(game, tc)
            game.herds[tp].cast_trait(self.card, self.trait_type, tc)

class DiscardTrait:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        self.player = args['player']
        self.card = args['card']

    def feasible(self, game):
        player_owns_trait = find_trait_herd(game, self.card) == self.player
        if player_owns_trait:
            return True, 'ok'
        else:
            return False, f"{self.player=} doesn't own {self.card=}"

    def apply(self, game):
        while game.herds[self.player].find_trait_index(self.card) != -1:
            game.herds[self.player].discard_trait(self.card)
        game.edisc.add(self.card)

class DiscardAnimal:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        self.player = args['player']
        self.card = args['card']

    def feasible(self, game):
        player_owns_animal = find_animal_herd(game, self.card) == self.player
        if player_owns_animal:
            return True, 'ok'
        else:
            return False, f"{self.player=} doesn't own {self.card=}"

    def apply(self, game):
        for c in game.herds[self.player].find_all_cards(self.card)[1:]:
            while game.herds[self.player].find_trait_index(c) != -1:
                game.herds[self.player].discard_trait(c)
            game.edisc.add(c)
        game.edisc.add(self.card)
        game.herds[self.player].discard_animal(self.card)

class SwapAnimals:
    def __init__(self, args):
        assert 'player' in args
        assert 'card1' in args
        assert 'card2' in args
        self.player = args['player']
        self.card1 = args['card1']
        self.card2 = args['card2']
        
    def feasible(self, game):
        card1_belongs = find_animal_herd(game, self.card1) == self.player 
        card2_belongs = find_animal_herd(game, self.card2) == self.player
        if card1_belongs and card2_belongs:
            return True, 'ok'
        else:
            return False, f"{card1_belongs=}; {card2_belongs}"

    @staticmethod
    def apply(self, game):
        idx1 = game.herds[self.player].find_animal_index(self.card1)
        idx2 = game.herds[self.player].find_animal_index(self.card2)
        tmp = game.herds[self.player].animals[idx1]
        game.herds[self.player].animals[idx1] = game.herds[self.player].animals[idx2]
        game.herds[self.player].animals[idx2] = tmp
        del tmp

class DrawCard:
    def __init__(self, args):
        assert 'player' in args
        player = args['player']
        self.player = player

    def feasible(self, game):
        has_cards = game.edeck.size() > 0 
        if has_cards:
            return True, 'ok'
        else:
            return False, 'no cards in evolution deck'

    def apply(self, game):
        game.hands[self.player].add(game.edeck.draw())

 


