from collections import defaultdict

class Library:
    def __init__(self):
        self.set_trait_req()
        self.set_area_red()
        self.set_area_grn()

    def set_trait_req(self):
        self.trait_req = defaultdict(lambda: 0, {
                    "carnivorous": 1,
                    "high_body_weight": 1,
                    "parasite": 2,
                    "detrimental_mutation": 1,
                    "stasis": 1
                })

    def get_trait_req(self, trait):
        return self.trait_req[trait]

    def set_area_red(self):
        self.area_red = defaultdict(lambda: 0, {
                "mangrove_forests": 2,
                "steppes":    2,
                "jungles":    3,
                "taiga":      3,
                "lakes":      2,
                "reed_beds":  2,
                "shrublands": 1,
                "caves":      2,
                "rocks":      1,
                "glaciers":   1,
                "tundra":     1,
                "savannahs":  2,
                "deserts":    1,
                "swamps":     1
            })

    def get_area_red(self, area):
        return self.area_red[area]

    def set_area_grn(self):
        self.area_grn = defaultdict(lambda: 0, {
                "mangrove_forests": 1,
                "jungles": 1,
                "shrublands": 1,
                "rocks":      1
            })
    
    def get_area_grn(self, area):
        return self.area_grn[area]

    def area_accessible(self, traits_txt, area):
        if area == 'caves': 
            return 'nocturnal' in traits_txt
        elif area == 'glaciers':
            return len(traits_txt) == 0
        elif area == 'savannah':
            return 'high_body_weight' in traits_txt
        elif area == 'lakes':
            return 'swimming' in traits_txt
        else:
            return True
