import math
import random

from Plant import *
from Cell import *
from NutritionTable import NutritionTable


class Grid:

    def step(self, time_multiplier):
        for row in self.cells:
            for cell in row:
                cell.step(time_multiplier)

    def get_neighbour_nutrition(self, pos, distance):
        nutrition = NutritionTable()
        nutrition.set_zero()
        for x in range(pos[0] - distance, pos[0] + distance + 1):
            for y in range(pos[1] - distance, pos[1] + distance + 1):
                if x < 0 or y < 0 or x >= len(self.cells) or y >= len(self.cells):
                    continue
                nutrition += self.cells[x][y].nutrition
        return nutrition

    def absorb_nutrition(self, pos, distance, nutrition):
        nut_per_cell = nutrition / math.pow(2 * distance + 1, 2)
        nutrition -= self.absorb_nutrition_helper(pos, distance, nut_per_cell)
        for x in range(pos[0] - distance, pos[0] + distance + 1):
            for y in range(pos[1] - distance, pos[1] + distance + 1):
                if x < 0 or y < 0 or x >= len(self.cells) or y >= len(self.cells):
                    continue
                nutrition -= self.cells[x][y].nutrition.absorb(nutrition)

    def absorb_nutrition_helper(self, pos, distance, nutrition):
        absorbed = NutritionTable()
        absorbed.set_zero()
        for x in range(pos[0] - distance, pos[0] + distance + 1):
            for y in range(pos[1] - distance, pos[1] + distance + 1):
                if x < 0 or y < 0 or x >= len(self.cells) or y >= len(self.cells):
                    continue
                absorbed += self.cells[x][y].nutrition.absorb(nutrition)
        return absorbed

    def __init__(self, *args):
        self.size = 5
        self.cells = [[Cell(0, 0, None, Plant(), None)]]
        self.p_list, p_size = create_plant_list()
        if len(args) == 0:
            self.cells = [[object for i in range(5)] for i in range(5)]
            for i in range(5):
                for j in range(5):
                    self.cells[i][j] = Cell(i, j, self.p_list, self.p_list[(random.randrange(p_size), 0)], self)
        elif len(args) == 1:
            premade_cells = args[0]
            self.cells = [[object for i in range(len(premade_cells))] for i in range(len(premade_cells[0]))]
            for i in range(len(self.cells)):
                for j in range(len(self.cells[0])):
                    self.cells[i][j] = premade_cells[i][j]

    def set_cell_data(self, x, y, plant, nutrition):
        if plant != None:
            self.cells[x][y].set_plant(plant)
        if nutrition != None:
            self.cells[x][y].set_nutrition(nutrition)


if __name__ == "__main__":
    random.seed(123)
    G = Grid()
    G.step(0.1)
    G.cells[0][0].plant.nutritionNeed.set([1, 1, 1])
    print(len(G.p_list.keys()))
