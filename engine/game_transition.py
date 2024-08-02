from engine.enum import AreaTextType as at, ItemType as it
from engine.evolution.animal import Animal
from engine.misc.stats import Stats

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
        stats = Stats()
        stats.add('req')
        stats.add('red')
        stats.add('blu')
        stats.add('grn')
        stats.add('fat')
        game.sdict[self.card] = stats
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
        player_has_card = game.hands[self.player].find_index(self.card) != -1
        one_or_two_targets = 0 < len(self.target_cards) < 3
        animals_in_herds = all([find_animal_herd(game, tc) != -1 for tc in self.target_cards])
        same_herd = len(set([find_animal_herd(game, tc) for tc in self.target_cards])) == 1
        if player_has_card and one_or_two_targets and animals_in_herds and same_herd:
            return True, 'ok'
        else:
            return False, f"{player_has_card=}; {one_or_two_targets=}; {animals_in_herds=}; {same_herd=}"

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

class PlaceArea:
    def __init__(self, args):
        pass

    def feasible(self, game):
        has_cards = game.adeck.size() > 0
        habitat_not_full = game.habitat.size() < game.num_players + 1
        if has_cards and habitat_not_full:
            return True, 'ok'
        else:
            return False, f'{has_cards=}; {habitat_not_full=}'

    def apply(self, game):
        area = game.adeck.draw()
        for sa in area:
            area_name = game.sadict[sa].get_text(at.NAME)
            stats = Stats()
            stats.add('red')
            stats.add('grn')
            stats.set('red', game.library.get_area_red(area_name))
            stats.set('grn', game.library.get_area_grn(area_name))
            game.sdict[sa] = stats
        game.habitat.place(area)

class RemoveArea:
    def __init__(self, args):
        pass

    def feasible(self, game):
        habitat_full = game.habitat.size() == game.num_players + 1
        if habitat_full:
            return True, 'ok'
        else:
            return False, f"{habitat_full=}"

    def apply(self, game):
        game.adisc.add(game.habitat.pop())

class UpdateStats:
    def __init__(self, args):
        pass

    def feasible(self, game):
        return True, 'ok'

    def apply(self, game):
        game.run_transition(UpdateAnimals, {})

class UpdateAnimals:
    def __init__(self, args):
        pass

    def feasible(self, game):
        return True, 'ok'

    def apply(self, game):
        for idx in range(game.num_players):
            herd = game.herds[idx]
            for animal in herd.animals:
                req = 1
                ac = Animal.card(animal)
                for tc, tt in Animal.traits(animal):
                    trait = game.edict[tc].get_trait(tt)
                    req += game.library.get_trait_req(trait)
                game.sdict[ac].set('req', req)

class TakeItem:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        assert 'target_card' in args
        assert 'item_type' in args
        self.player       = args['player']
        self.card         = args['card']
        self.target_card  = args['target_card']
        self.item_type    = args['item_type']

    def feasible(self, game):
        owner = find_animal_herd(game, self.card)
        idx = game.herds[owner].find_animal_index(self.card)
        animal = game.herds[owner].get(idx)
        player_owns_animal = owner == self.player
        area_in_habitat = game.habitat.contains(self.target_card)
        area_has_item = game.sdict[self.target_card].get(self.item_type) > 0
        area_accessible = game.library.area_accessible(Animal.traits_txt(animal, game.edict), 
                                                       game.sadict[self.target_card].get_text(at.NAME))
        food_allowed = True
        if self.item_type in [it.RED, it.BLUE]:
            food_allowed = game.sdict[self.card].get('req') > \
                           game.sdict[self.card].get('blu') + \
                           game.sdict[self.card].get('red')
        shelter_allowed = True
        if self.item_type == it.GREEN:
            shelter_allowed = game.sdict[self.card].get('grn') == 0 or \
                              Animal.has_trait(animal, game.edict, 'xylophagous')
        if player_owns_animal and \
           area_in_habitat and \
           area_accessible and \
           area_has_item and \
           food_allowed and \
           shelter_allowed:
            return True, 'ok'
        else:
            return False, f'{player_owns_animal=}' + \
                   f' {area_in_habitat=}' + \
                   f' {area_accessible=}' + \
                   f' {area_has_item=}' + \
                   f' {food_allowed=}' + \
                   f' {shelter_allowed=}'

    def apply(self, game):
        game.sdict[self.card].increment(self.item_type)
        game.sdict[self.target_card].decrement(self.item_type)
