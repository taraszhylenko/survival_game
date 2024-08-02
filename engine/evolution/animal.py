from engine.render import Render

class Animal:
    @staticmethod
    def create(idx):
        return [idx]

    @staticmethod
    def add_trait(card_list, idx, trait_type):
        return card_list + [(idx, trait_type)]

    @staticmethod
    def remove_trait(card_list, idx):
        return card_list[:1] + list(filter(lambda x: x[0] != idx, card_list[1:]))

    @staticmethod
    def render(card_list, card_dict):
        idx    = card_list[0]
        traits = card_list[1:]
        render = card_dict[idx].render_back(True)
        for idx, trait_type in traits:
            render = render.stack_below(card_dict[idx].render_trait(trait_type, True), True)
        return render

    @staticmethod
    def card(card_list):
        return card_list[0]

    @staticmethod
    def traits(card_list):
        return card_list[1:]

    @staticmethod
    def traits_txt(card_list, card_dict):
        return [card_dict[c].get_trait(t) for c, t in card_list[1:]]

    @staticmethod
    def has_trait(card_list, card_dict, trait):
        return any([card_dict[c].get_trait(t) == trait \
                    for c, t in card_list[1:]])
