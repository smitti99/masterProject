import random
import sys

from HelperFunctions import *


class NutritionTable:

    def __init__(self, *args):
        size = -1
        if len(args) > 0:
            size = len(args)
        self.dir = {'K': -1, 'P': -1, 'N': -1}
        for pos, key in enumerate(self.dir):
            if pos < size:
                self.dir[key] = args[pos]
            else:
                self.dir[key] = random.randrange(3, 5)

    def get_dir(self):
        return self.dir

    def set_dir(self, dir):
        self.dir = dir

    def set(self, values):
        for pos, key in enumerate(self.dir):
            self.dir[key] = values[pos]

    def set_zero(self):
        for key in self.dir:
            self.dir[key] = 0

    def get_min_rate(self, other):
        keys = list(self.dir.keys())
        min = sys.float_info.max
        for key in keys:
            if other.dir[key] <= 0:
                continue
            check = self.dir[key] / other.dir[key]
            if check < min:
                min = check
        return min

    def __mul__(self, other):
        new_dir = self.dir.copy()
        for key in new_dir.keys():
            new_dir[key] *= other
        new_table = NutritionTable()
        new_table.set(list(new_dir.values()))
        return new_table

    def __iadd__(self, other):
        for key in self.dir.keys():
            self.dir[key] += other.dir[key]
        return self

    def __truediv__(self, other):
        new_dir = self.dir.copy()
        backup = self.dir.copy()
        for key in new_dir.keys():
            new_dir[key] /= other
        new_table = NutritionTable()
        new_table.dir = new_dir
        self.dir = backup
        return new_table

    def __isub__(self, other):
        for key in self.dir.keys():
            self.dir[key] -= other.dir[key]
        return self

    def is_zero(self):
        for key in self.dir:
            if self.dir[key] > 0:
                return False
        return True

    def absorb(self, other):
        absorbed = NutritionTable()
        for key in self.dir:
            if self.dir[key] < other.dir[key]:
                absorbed.get_dir()[key] = self.dir[key]
                self.dir[key] = 0
            else:
                self.dir[key] -= other.dir[key]
                absorbed.get_dir()[key] = other.dir[key]
        return absorbed
