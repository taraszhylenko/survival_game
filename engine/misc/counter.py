from engine.render import Render

class Counter:
    def __init__(self, label, value):
        self.label = label
        self.value = value

    def increment(self):
        self.value += 1
        assert 0 <= self.value < 100

    def decrement(self):
        self.value -= 1
        assert 0 <= self.value < 100

    def render(self):
        return Render.from_string(f'{self.label}: {self.value}')
