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
    def from_string(string_):
        arr = []
        for char in string_: 
            arr.append(ord(char))
        return Render(np.array([arr]))

    @staticmethod
    def blank(h, l):
        return Render(np.ones((h, l), dtype=int) * ord(' '))

    def copy(self):
        return Render(self.arr.copy())

    def pad(self, direction, char):
        num = ord(char)
        if direction == 'up':
            bot = self.arr
            top = np.array([[num] * self.l])
            return Render(np.concatenate([top, bot], axis=0))
        elif direction == 'right':
            left  = self.arr
            right = np.array([[num]] * self.h)
            return Render(np.concatenate([left, right], axis=1))
        elif direction == 'down':
            top = self.arr
            bot = np.array([[num] * self.l])
            return Render(np.concatenate([top, bot], axis=0))
        elif direction == 'left':
            right = self.arr
            left  = np.array([[num]] * self.h)
            return Render(np.concatenate([left, right], axis=1))
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
        assert other.h <= self.h - i and other.l <= self.l - j, f"{other.h=}, {self.h=}, {i=}, {other.l=}, {self.l=}, {j=}"
        new_arr = self.arr.copy()
        new_arr[i:i+other.h, j:j+other.l] = other.arr
        return Render(new_arr)

    def insert_tag_br(self, tag):
        tag_render = Render.from_string(tag)
        return self.insert_from(tag_render, self.h - 1, self.l - 1 - tag_render.l)

    def add_border(self, tight_down):
        if tight_down: 
            tmp = self.replace_row(-1, ' ', '_')
        else:
            tmp = self.pad('down',  '_')
        return tmp.pad('left',  '|' \
                 ).pad('right', '|' \
                 ).pad('up',    '_')

    def replace_row(self, row_idx, from_, to_):
        from_int = ord(from_)
        to_int   = ord(to_)
        new_arr = self.arr.copy()
        for i in range(self.l):
            if new_arr[row_idx, i] == from_int:
                new_arr[row_idx, i] = to_int
        return Render(new_arr)


    def balloon_to(self, h, l):
        target = self.copy()
        assert target.h <= h and target.l <= l
        dirs = ['up', 'right', 'down', 'left']
        idx = 0
        while h > target.h or l > target.l:
            if dirs[idx] in {'up', 'down'} and h > target.h:
                target = target.pad(dirs[idx], ' ')
            elif dirs[idx] in {'left', 'right'} and l > target.l:
                target = target.pad(dirs[idx], ' ')
            idx = (idx + 1) % 4
        return target

    @staticmethod
    def merge_into_row(renders):
        h = max([r.h for r in renders])
        l = sum([r.l for r in renders]) 
        out = Render.blank(h, l)
        cuml = 0
        for i, r in enumerate(renders):
            out = out.insert_from(r, h - r.h, cuml)
            cuml += r.l
        return out

    @staticmethod
    def merge_into_column(renders):
        h = sum([r.h for r in renders])
        l = max([r.l for r in renders]) 
        out = Render.blank(h, l)
        cumh = 0
        for r in renders:
            out = out.insert_from(r, cumh, 0)
            cumh += r.h
        return out

    def print(self):
        for i in range(self.h):
            for j in range(self.l):
                print(chr(self.arr[i,j]), end='')
            print()
