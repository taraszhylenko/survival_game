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
                rows.append([ord(ch) for ch in row])
        return Render(np.array(rows))

    def print(self):
        for i in range(self.h):
            for j in range(self.l):
                print(chr(self.arr[i,j]), end='')
