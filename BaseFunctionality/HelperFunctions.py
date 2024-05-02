import math

import numpy

import GlobalConfig
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


def get_yield_from_plantlst(plantlist):
    plants, size = plantlist
    yields = [0 for i in range(size)]
    keys = list(plants.keys())
    for key in keys:
        if plants[key].harvest > yields[key[0]]:
            yields[key[0]] = plants[key].harvest
    return yields


def nutrition_to_cost(nutrition):
    cost = 0
    for key in nutrition.dir.keys():
        cost += nutrition.dir[key] * GlobalConfig.fertilizer_cost[key]
    return cost


def evaluate_nutrition_value(nutrition):
    keys = nutrition.dir.keys()
    guidlines = GlobalConfig.nutrition_guidelines
    value = 0
    for key in keys:
        # above perfect minimum
        if nutrition.dir[key] > guidlines[key][1]:
            # below perfect maximum
            if nutrition.dir[key] < guidlines[key][2]:
                continue
            # below acceptable maximum
            elif nutrition.dir[key] < guidlines[key][3]:
                value += nutrition.dir[key] - guidlines[key][2]
            # above acceptable maximum
            else:
                value += math.pow(nutrition.dir[key] - guidlines[key][2], 2)
        # above acceptable minimum
        elif nutrition.dir[key] > guidlines[key][0]:
            value += guidlines[key][1] - nutrition.dir[key]
        # below acceptable minimum
        else:
            value += pow(guidlines[key][1] - nutrition.dir[key], 2)
    return value
