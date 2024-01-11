import datetime
import json
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
    for x in range(size):
        for y in range(size):
            min_error = float("inf")
            for i, need in enumerate(nutrition_needs):
                e = Helper.square_error(list(need.dir.values()), list(new[x][y].values()))
                if e < min_error:
                    plants[x][y] = plant_list[0][(i, 0)]
                    plant_id[x][y] = i
                    plant_error[x][y] = e
                    min_error = e

    with open(os.path.join(GlobalConfig.log_path, "plant.json"), "w") as f:
        json.dump({"plant_ids": plant_id, "error": plant_error}, f)
    print("     Starting simulation at " + str(datetime.datetime.now().time()))
    G = Grid.Grid(new, plants)
    for i in range(step_number):
        G.step(time_multiplier)
    G.log_nutrition()


def grid(time_multiplier, step_number, nut):
    GlobalConfig.log_path = askdirectory(title='Select Log Folder for Grid Greedy')
    print("     Starting evaluation at " + str(datetime.datetime.now().time()))
    plant_list = Plant.create_plant_list()
    nutrition_needs = Helper.get_need_from_plantlist(plant_list)
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
    plant = -1
    min_error = float("inf")
    for i, need in enumerate(nutrition_needs):
        e = Helper.square_error(list(need.dir.values()), list(avg_nutrtion.dir.values()))
        if e < min_error:
            plant = i
            min_error = e

    with open(os.path.join(GlobalConfig.log_path, "plant.json"), "w") as f:
        json.dump({"plant_id": plant}, f)
    plants = [[plant_list[0][(plant, 0)] for y in range(size)] for x in range(size)]
    print("     Starting simulation at " + str(datetime.datetime.now().time()))
    G = Grid.Grid(reversed_nutrition, plants)
    for i in range(step_number):
        G.step(time_multiplier)
    G.log_nutrition()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file = tk.filedialog.askopenfilename(title="Select Nutrition-File")
    with open(file) as f:
        nut = json.load(f)
    timeMult = 1
    stepNum = 250
    print("Starting Grid at " + str(datetime.datetime.now().time()))
    grid(timeMult, stepNum, nut)
    print("Finished Grid at " + str(datetime.datetime.now().time()))
    print("Starting Single at " + str(datetime.datetime.now().time()))
    single_cell(timeMult, stepNum, nut)
    print("Finished Single at " + str(datetime.datetime.now().time()))
