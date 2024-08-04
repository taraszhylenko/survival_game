from engine.render import Render

class Stats:
    def __init__(self):
        self.stats = dict()

    def add(self, key):
        assert isinstance(key, str)
        assert len(key) <= 3
        self.stats[key] = 0

    def increment(self, key):
        self.stats[key] += 1
        assert 0 <= self.stats[key] < 100

    def decrement(self, key):
        self.stats[key] -= 1
        assert 0 <= self.stats[key] < 100

    def decrement_one_of(self, keys):
        for key in keys:
            if self.stats[key] > 0:
                self.stats[key] -= 1
                return
        assert False

    def set(self, key, value):
        assert isinstance(key, str)
        assert len(key) <= 3
        assert key in self.stats
        assert 0 <= value < 100
        self.stats[key] = value

    def render(self):
        return Render.merge_column([Render.from_string(f'{k}: {v}') for k, v in self.stats.items()])

    def get(self, key):
        return self.stats[key]
