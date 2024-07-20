import numpy as np

class Render:
    def __init__(self, arr):
        self.arr = arr
        self.h, self.l = arr.shape

    @staticmethod
    def from_txt(txt_file):
        rows = list()
        with open(txt_file, 'r') as f:
            for row in f:
                rows.append([ord(ch) for ch in row[:-1]])
        return Render(np.array(rows))
   
    @staticmethod
    def blank(height, length):
        return Render(np.ones((height, length), dtype=int) * ord(' '))

    def pad(self, direction, char):
        num = ord(char)
        if direction == 'up':
            return Render(np.concatenate([np.array([[num] * self.l]), self.arr], axis=0))
        elif direction == 'right':
            return Render(np.concatenate([self.arr, np.array([[num]] * self.h)], axis=1))
        elif direction == 'down':
            return Render(np.concatenate([self.arr, np.array([[num] * self.l])], axis=0))
        elif direction == 'left':
            return Render(np.concatenate([np.array([[num]] * self.h), self.arr], axis=1))
        else:
            raise AssertionError(f'{direction=}, should be one of [up, right, down, left]')

    def stack_above(self, other, weld):
        assert isinstance(weld, bool)
        assert isinstance(other, Render)
        assert self.l == other.l
        return Render(np.concatenate([self.arr, other.arr[1 if weld else 0:]]))

    def stack_below(self, other, weld):
        assert isinstance(other, Render)
        return other.stack_above(self, weld)

    def insert_from(self, other, i, j):
        assert isinstance(other, Render)
        assert other.h <= self.h - i and other.l <= self.l - j
        new_arr = self.arr.copy()
        new_arr[i:i+other.h, j:j+other.l] = other.arr
        return Render(new_arr)

    def print(self):
        for i in range(self.h):
            for j in range(self.l):
                print(chr(self.arr[i,j]), end='')
            print()
