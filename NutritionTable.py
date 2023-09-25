from HelperFunctions import *


class NutritionTable:
    dir = {'K': -1, 'P': -1, 'N': -1}

    def compare(self, other):
        return avg([other.K / self.K, other.N / self.N, other.P / self.P])

    def get_min_rate(self, other):
        keys = self.dir.keys()
        min = self.dir[keys[0]] / other.dir[keys[0]]
        for key in keys:
            check = self.dir[key] / other.dir[key]
            if check < min:
                min = check
        return min

    def __mul__(self, other):
        new_dir = self.dir.copy()
        for key in new_dir.keys():
            new_dir[key] *= other
        new_table = NutritionTable()
        new_table.dir = new_dir
        return new_table
