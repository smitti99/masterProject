import numpy
from BaseFunctionality import NutritionTable


def avg(values):
    sum = 0.0
    count = 0.0
    for value in values:
        sum += value
        count += 1
    return sum / count


def min(values):
    min = values[0]
    for value in values:
        if value < min:
            min = value
    return min


def convert_nutrition_array(old):
    keys = list(old.keys())
    size = len(old[keys[0]])
    new = [[{} for x in range(size)] for y in range(size)]
    for key in keys:
        for x in range(size):
            for y in range(size):
                new[x][y].update({key: old[key][x][y]})
    return new


def square_error(list_a, list_b):
    e = 0
    for i in range(len(list_b)):
        e += numpy.square(list_a[i] - list_b[i])
    return e

def real_error(list_a, list_b):
    e = 0
    for i in range(len(list_b)):
        e += list_a[i] - list_b[i]
    return e


def get_need_from_plantlist(plant_list):
    plants, size = plant_list
    nuts = [NutritionTable.NutritionTable() for i in range(size)]
    for nut in nuts:
        nut.set_zero()
    keys = list(plants.keys())
    for key in keys:
        nuts[key[0]] += plants[key].nutritionNeed * plants[key].timeToGrow
    return nuts
