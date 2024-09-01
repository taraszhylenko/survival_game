from engine.enum import AreaTextType as at, ItemType as it
from engine.evolution.animal import Animal
from engine.misc.stats import Stats


class CastAnimal:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        self.p = args['player']
        self.c = args['card']
    
    def feasible(self, game):
        controls = game.hands[self.p].find_index(self.c) != -1
        if controls:
            return True, 'ok'
        else:
            return False, f"{controls=}"

    def apply(self, game):
        stats = Stats()
        stats.add('req')
        stats.add('red')
        stats.add('blu')
        stats.add('grn')
        stats.add('fat')
        game.sdict[self.c] = stats
        game.hands[self.p].discard(self.c)
        game.herds[self.p].cast_animal(self.c)

class CastTrait:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        assert 'trait_type' in args
        assert 'target_cards' in args
        self.p   = args['player']
        self.c   = args['card']
        self.tt  = args['trait_type']
        self.tcs = args['target_cards']

    def feasible(self, game):
        holds = game.find_hand_owner(self.c) == self.p
        txt = game.edict[self.c].get_trait(self.tt)
        appropriate_targets = len(self.tcs) == game.library.get_trait_num_targets(txt)
        os = [game.find_animal_owner(tc) for tc in self.tcs]
        animals_in_herds = all([o != -1 for o in os])
        same_herd = len(set(os)) == 1
        detrimental_check = game.library.detrimental_check(txt, os[0] == self.p)
        can_add_trait = all([Animal.can_add_trait(game.find_animal(tc), game.edict, txt) for tc in self.tcs])
        if holds and \
            appropriate_targets and \
            animals_in_herds and \
            detrimental_check and \
            can_add_trait and \
            same_herd:
            return True, 'ok'
        else:
            return False, f"{holds=}; {appropriate_targets=}; {animals_in_herds=}; {same_herd=}; {detrimental_check=}; {can_add_trait=}"

    def apply(self, game):
        game.hands[self.p].discard(self.c)
        for tc in self.tcs:
            tp = game.find_animal_owner(tc)
            game.herds[tp].cast_trait(self.c, self.tt, tc)

class DiscardTrait:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        self.p = args['player']
        self.c = args['card']

    def feasible(self, game):
        controls = game.find_trait_owner(self.c) == self.p
        if controls:
            return True, 'ok'
        else:
            return False, f"{controls=}"

    def apply(self, game):
        while game.herds[self.p].find_trait_index(self.c) != -1:
            game.herds[self.p].discard_trait(self.c)
        game.edisc.add(self.c)

class DiscardAnimal:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        self.p = args['player']
        self.c = args['card']

    def feasible(self, game):
        controls = game.find_animal_owner(self.c) == self.p
        if controls:
            return True, 'ok'
        else:
            return False, f"{controls=}"

    def apply(self, game):
        for c in game.herds[self.p].find_all_cards(self.c)[1:]:
            while game.herds[self.p].find_trait_index(c) != -1:
                game.herds[self.p].discard_trait(c)
            game.edisc.add(c)
        game.edisc.add(self.c)
        game.herds[self.p].discard_animal(self.c)

class SwapAnimals:
    def __init__(self, args):
        assert 'player' in args
        assert 'card1' in args
        assert 'card2' in args
        self.p = args['player']
        self.c1 = args['card1']
        self.c2 = args['card2']
        
    def feasible(self, game):
        controls1 = game.find_animal_owner(self.c1) == self.p 
        controls2 = game.find_animal_owner(self.c2) == self.p
        if controls1 and controls2: 
            return True, 'ok'
        else:
            return False, f"{controls1=}; {controls2=}"

    def apply(self, game):
        idx1 = game.find_animal_index(self.c1)
        idx2 = game.find_animal_index(self.c2)
        tmp = game.find_animal(self.c1)
        game.herds[self.p].animals[idx1] = game.find_animal(self.c2)
        game.herds[self.p].animals[idx2] = tmp
        del tmp

class DrawCard:
    def __init__(self, args):
        assert 'player' in args
        self.p = args['player']

    def feasible(self, game):
        deck_nonempty = game.edeck.size() > 0 
        if deck_nonempty:
            return True, 'ok'
        else:
            return False, f'{deck_nonempty=}'

    def apply(self, game):
        game.hands[self.p].add(game.edeck.draw())

class PlaceArea:
    def __init__(self, args):
        pass

    def feasible(self, game):
        deck_nonempty = game.adeck.size() > 0
        habitat_not_full = game.habitat.size() < game.num_players + 1
        if deck_nonempty and habitat_not_full:
            return True, 'ok'
        else:
            return False, f'{deck_nonempty=}; {habitat_not_full=}'

    def apply(self, game):
        aa = game.adeck.draw()
        for sa in aa:
            name = game.sadict[sa].get_text(at.NAME)
            stats = Stats()
            stats.add('red')
            stats.add('grn')
            stats.set('red', game.library.get_area_red(name))
            stats.set('grn', game.library.get_area_grn(name))
            game.sdict[sa] = stats
        game.habitat.place(aa)

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
        for p in range(game.num_players):
            herd = game.herds[p]
            for a in herd.animals:
                req = 1
                c = Animal.card(a)
                for tc, tt in Animal.traits(a):
                    txt = game.edict[tc].get_trait(tt)
                    req += game.library.get_trait_req(txt)
                game.sdict[c].set('req', req)

class TakeItem:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        assert 'target_card' in args
        assert 'item_type' in args
        self.p  = args['player']
        self.c  = args['card']
        self.tc = args['target_card']
        self.it = args['item_type']

    def feasible(self, game):
        if not game.is_animal(self.c):
            return False, "card is not an animal"
        elif not game.habitat.contains(self.tc):
            return False, "area not in habitat"
        controls = game.find_animal_owner(self.c) == self.p
        area_has_item = game.subarea_has_item(self.tc, self.it)
        area_accessible = game.subarea_accessible(self.c, self.tc)
        
        can_eat = True
        if self.it in [it.RED, it.BLUE]:
            can_eat = game.can_eat(self.c)

        can_hide = True
        if self.it == it.GREEN:
            can_hide = game.can_hide(self.c)

        if controls and \
           area_accessible and \
           area_has_item and \
           can_eat and \
           can_hide:
            return True, 'ok'
        else:
            return False, f'{controls=}' + \
                   f' {area_has_item=}' + \
                   f' {area_accessible=}' + \
                   f' {can_eat=}' + \
                   f' {can_hide=}'

    def apply(self, game):
        game.sdict[self.c].increment(self.it)
        game.sdict[self.tc].decrement(self.it)
        if self.it == it.GREEN and 'xylophagous' in game.animal_traits(self.c):
            if game.can_eat(self.c):
                game.sdict[self.c].increment(it.BLUE)

class ConvertFat:
    def __init__(self, args):
        pass

    def feasible(self, game):
        return True, 'ok'

    def apply(self, game):
        for p in range(game.num_players):
            for idx, a in enumerate(game.herds[p].animals):
                for i in range(Animal.num_food(a, game.sdict) - \
                               Animal.num_req(a, game.sdict)):
                    game.sdict[a[0]].increment(it.FAT)
                    game.sdict[a[0]].decrement_one_of([it.RED, it.BLUE])

class RunExtinction:
    def __init__(self, args):
        pass

    def feasible(self, game):
        return True, 'ok'

    def apply(self, game):
        for p in range(game.num_players):
            for c in game.herds[p].animal_cards():
                if not game.can_survive(c):
                    game.run_transition(DiscardAnimal, {'player': p,
                                                        'card': c})
                else:
                    for _ in range(Animal.num_req(game.find_animal(c), game.sdict)):
                        game.sdict[c].decrement_one_of([it.RED, it.BLUE, it.FAT])
                    game.sdict[c].set(it.GREEN, 0)

class EatAnimal:
    def __init__(self, args):
        assert 'player' in args
        assert 'card' in args
        assert 'target_card' in args
        self.p  = args['player']
        self.c  = args['card']
        self.tc = args['target_card']
        self.tcs2 = args['ignore_cards']

    def feasible(self, game):
        controls = game.find_animal_owner(self.c) == self.p

    def apply(self, game):
        pass
