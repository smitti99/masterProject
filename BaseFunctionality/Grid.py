import json
import math
import random
import time

import GlobalConfig
from BaseFunctionality.Plant import *
from BaseFunctionality.Cell import *
from BaseFunctionality.NutritionTable import NutritionTable


class Grid:

    def step(self, time_multiplier):
        if GlobalConfig.log_nutrition:
            self.log_nutrition()
        if GlobalConfig.log_yield:
            self.log_yield()
        for row in self.cells:
            for cell in row:
                cell.step(time_multiplier)
        GlobalConfig.global_step += 1
        GlobalConfig.global_step_char = "'" + str(GlobalConfig.global_step) + "'"

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
        elif len(args)== 2:
            nutritions = args[0]
            plants = args[1]
            self.cells = [[object for i in range(5)] for i in range(5)]
            for i in range(5):
                for j in range(5):
                    self.cells[i][j] = Cell(i, j, self.p_list, plants[i][j], self)
                    self.cells[i][j].nutrition.set_dir(nutritions[i][j])
        GlobalConfig.size = len(self.cells)

    def set_cell_data(self, x, y, plant, nutrition):
        if plant != None:
            self.cells[x][y].set_plant(plant)
        if nutrition != None:
            self.cells[x][y].set_nutrition(nutrition)

    def log_nutrition(self):
        file_name = GlobalConfig.log_path + "/nutrition.json"
        try:
            with open(file_name) as f:
                js = json.load(f)
        except:
            js = {}
        data = {}
        size = len(self.cells)
        keys = self.cells[0][0].nutrition.dir.keys()
        for key in keys:
            data.update({key: [[0 for i in range(size)] for i in range(size)]})
        for x in range(size):
            for y in range(size):
                for key in keys:
                    data[key][x][y] = self.cells[x][y].nutrition.dir[key]

        js.update({GlobalConfig.global_step: data})
        with open(file_name, "w") as f:
            json.dump(js, f)

    def log_yield(self):
        file_name = GlobalConfig.log_path + "/yield.json"
        try:
            with open(file_name) as f:
                js = json.load(f)
                if not GlobalConfig.global_step_char in js or \
                        len(js[GlobalConfig.global_step_char]) >= GlobalConfig.size * GlobalConfig.size:
                    js.update({GlobalConfig.global_step_char: []})
        except:
            js = {GlobalConfig.global_step_char: []}
        for row in self.cells:
            for cell in row:
                js[GlobalConfig.global_step_char].append(cell.plant.harvest)
        with open(file_name,"w") as f:
            json.dump(js, f)
