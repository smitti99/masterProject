import datetime
import json
import math
import os
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory

import BaseFunctionality.HelperFunctions as Helper
import BaseFunctionality.Plant as Plant
import BaseFunctionality.Grid as Grid
import GlobalConfig
import cProfile

from BaseFunctionality.NutritionTable import NutritionTable


def single_cell(time_multiplier, step_number, nut):
    GlobalConfig.log_path = askdirectory(title='Select Log Folder for Single Cell Greedy')
    print("     Starting evaluation at " + str(datetime.datetime.now().time()))
    new = Helper.convert_nutrition_array(nut)
    size = len(new)
    plant_list = Plant.create_plant_list()
    nutrition_needs = Helper.get_need_from_plantlist(plant_list)
    plants = [[-1 for x in range(size)] for y in range(size)]
    plant_id = [[-1 for x in range(size)] for y in range(size)]
    plant_error = [[-1 for x in range(size)] for y in range(size)]
    plant_yields = Helper.get_yield_from_plantlst(plant_list)
    guideline = NutritionTable(GlobalConfig.nutrition_guidelines["K"][1], GlobalConfig.nutrition_guidelines["P"][1],
                               GlobalConfig.nutrition_guidelines["N"][1])
    fertelizer = NutritionTable()
    fertelizer.set_zero()
    total_cost = 0
    for x in range(size):
        for y in range(size):
            best_cost = 0
            best_ratio = -1
            best_fert = NutritionTable()
            available = NutritionTable()
            available.set_dir(new[x][y])
            for i, need in enumerate(nutrition_needs):
                fert = NutritionTable()
                diff = available - guideline
                fert = need - diff
                cost = Helper.nutrition_to_cost(fert)
                if cost <= 0:
                    cost = 1
                ratio = plant_yields[i] / cost
                if ratio > best_ratio:
                    plants[x][y] = plant_list[0][(i, 0)]
                    plant_id[x][y] = i
                    best_fert = fert
                    best_ratio = ratio
                    best_cost = cost
            total_cost += best_cost / (math.pow(size, 2))
            fertelizer += best_fert / (math.pow(size, 2))

    print("     Starting simulation at " + str(datetime.datetime.now().time()))
    G = Grid.Grid(new, plants)
    G.to_fertilize = True
    G.fertilizer = fertelizer * time_multiplier / step_number
    for i in range(step_number):
        G.step(time_multiplier)
    nutrition_error = 0
    plant_yield = 0
    for x in range(5):
        for y in range(5):
            plant_yield += G.cells[x][y].plant.harvest
            nutrition_error += Helper.evaluate_nutrition_value(G.cells[x][y].nutrition)
    cost = Helper.nutrition_to_cost(G.fertilizer) * step_number * 25
    with open(os.path.join(GlobalConfig.log_path, "info.json"), "w") as f:
        json.dump({"plant_ids": plant_id, "yield": plant_yield / 25, "nutrition_error": nutrition_error / 25,
                   "cost": cost, "fertelizer": list(G.fertilizer.dir.values())}, f)
    G.log_nutrition()


def grid(time_multiplier, step_number, nut):
    GlobalConfig.log_path = askdirectory(title='Select Log Folder for Grid Greedy')
    print("     Starting evaluation at " + str(datetime.datetime.now().time()))
    plant_list = Plant.create_plant_list()
    nutrition_needs = Helper.get_need_from_plantlist(plant_list)
    plant_yields = Helper.get_yield_from_plantlst(plant_list)
    avg_nutrtion = NutritionTable()
    avg_nutrtion.set_zero()
    reversed_nutrition = Helper.convert_nutrition_array(nut)
    for row in reversed_nutrition:
        for cell in row:
            tmp = NutritionTable()
            tmp.set_dir(cell)
            avg_nutrtion += tmp
    size = len(reversed_nutrition)
    avg_nutrtion = avg_nutrtion / (size * size)
    guideline = NutritionTable(GlobalConfig.nutrition_guidelines["K"][1], GlobalConfig.nutrition_guidelines["P"][1],
                               GlobalConfig.nutrition_guidelines["N"][1])
    diff = avg_nutrtion - guideline
    plant = -1
    best_ratio = -1
    best_fertelizer = NutritionTable()
    for i, need in enumerate(nutrition_needs):
        fertilizer = NutritionTable()
        fertilizer = need - diff
        cost = Helper.nutrition_to_cost(fertilizer)
        if cost <= 0:
            cost = 1
        ratio = plant_yields[i] / cost
        if ratio > best_ratio:
            plant = i
            best_ratio = ratio
            best_fertelizer = fertilizer
    cost = Helper.nutrition_to_cost(best_fertelizer)

    plants = [[plant_list[0][(plant, 0)] for y in range(size)] for x in range(size)]
    print("     Starting simulation at " + str(datetime.datetime.now().time()))
    G = Grid.Grid(reversed_nutrition, plants)
    G.to_fertilize = True
    G.fertilizer = best_fertelizer * time_multiplier / step_number
    for i in range(step_number):
        G.step(time_multiplier)
    nutrition_error = 0
    plant_yield = 0
    cost = Helper.nutrition_to_cost(G.fertilizer) * step_number * 25
    for x in range(5):
        for y in range(5):
            plant_yield += G.cells[x][y].plant.harvest
            nutrition_error += Helper.evaluate_nutrition_value(G.cells[x][y].nutrition)
    with open(os.path.join(GlobalConfig.log_path, "info.json"), "w") as f:
        json.dump({"plant_id": plant, "yield": plant_yield / 25, "nutrition_error": nutrition_error / 25, "cost": cost,
                   "fertelizer": list(G.fertilizer.dir.values())}, f)
    G.log_nutrition()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file = tk.filedialog.askopenfilename(title="Select Nutrition-File")
    with open(file) as f:
        nut = json.load(f)
    timeMult = 1
    stepNum = 250
    GlobalConfig.log_yield = True
    GlobalConfig.log_growth = True
    GlobalConfig.log_nutrition = False
    print("Starting Single at " + str(datetime.datetime.now().time()))
    single_cell(timeMult, stepNum, nut)
    print("Finished Single at " + str(datetime.datetime.now().time()))
    print("Starting Grid at " + str(datetime.datetime.now().time()))
    grid(timeMult, stepNum, nut)
    print("Finished Grid at " + str(datetime.datetime.now().time()))
