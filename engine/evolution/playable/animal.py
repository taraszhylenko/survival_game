from engine.render import Render

class Animal:
    def __init__(self, idx):
        self.idx  = idx
        self.traits   = list()
    
    def add_trait(self, idx, trait_type):
        self.traits.append((idx, trait_type))

    def remove_trait(self, idx):
        self.traits = list(filter(lambda x: x[0] != idx, self.traits))

    def update_req(self, evolution_dict):
        req = 1

    def render(self, evolution_dict):
        render = evolution_dict[self.idx].render_back(True)
        for idx, trait_type in self.traits:
            render = render.stack_below(evolution_dict[idx].render_trait(trait_type, True), True)
        return render
