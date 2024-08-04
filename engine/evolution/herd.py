from engine.render import Render
from engine.evolution.animal import Animal

class Herd:
    def __init__(self):
        self.animals = list()

    def cast_animal(self, card):
        self.animals.append(Animal.create(card))

    def find_animal_index(self, card):
        idx = -1
        for i in range(len(self.animals)):
            if self.animals[i][0] == card:
                idx = i
        return idx

    def find_trait_index(self, card):
        idx = -1
        for i in range(len(self.animals)):
            for t in self.animals[i][1:]:
                if t[0] == card:
                    idx = i
        return idx

    def find_index(self, card):
        return max([-1, self.find_animal_index(card), self.find_trait_index(card)])

    def cast_trait(self, card, trait_type, target_card):
        idx = self.find_index(target_card)
        assert idx != -1, f"player doesn't have {target_card} in herd"
        self.animals[idx] = Animal.add_trait(self.animals[idx], card, trait_type)

    def discard_trait(self, card):
        idx = self.find_index(card)
        assert idx != -1, f"player doesn't have {card} in traits"
        self.animals[idx] = Animal.remove_trait(self.animals[idx], card)

    def find_all_cards(self, card):
        idx = self.find_index(card)
        assert idx != -1
        return [self.animals[idx][0]] + [c[0] for c in self.animals[idx][1:]]

    def discard_animal(self, card):
        idx = self.find_index(card)
        assert idx != -1
        assert len(self.animals[idx]) == 1
        self.animals.pop(idx)

    def swap_animals(self, card1, card2):
        idx1 = self.find_index(card1)
        idx2 = self.find_index(card2)
        assert idx1 != -1
        assert idx2 != -1
        tmp = self.animals[idx1]
        self.animals[idx1] = self.animals[idx2]
        self.animals[idx2] = tmp
        del tmp

    def render(self, card_dict):
        return Render.merge_row([Animal.render(a, card_dict) for a in self.animals])

    def render_stats(self, stat_dict, h, l):
        stats = [stat_dict[a[0]].render() for a in self.animals] 
        return Render.merge_row([stat.balloon_to(stat.h, l) for stat in stats])
    
    def get(self, idx):
        return self.animals[idx] 

    def animal_cards(self):
        return [a[0] for a in self.animals]

