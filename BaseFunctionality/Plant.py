import json

import GlobalConfig
from BaseFunctionality.NutritionTable import NutritionTable


class Plant:
    ID = -1
    growStep = -1
    absorbRange = -1
    timeToGrow = -1
    harvest = -1
    nutritionNeed = NutritionTable()

    def step(self, time_multiplier, nutritions):


        try:
            with open(GlobalConfig.log_path + "/growth.json") as f:
                js = json.load(f)
                if not GlobalConfig.global_step_char in js or \
                        len(js[GlobalConfig.global_step_char]) >= GlobalConfig.size * GlobalConfig.size:
                    js.update({GlobalConfig.global_step_char: []})
        except:
            js = {GlobalConfig.global_step_char: []}
        if self.timeToGrow >= 0:
            rate = nutritions.get_min_rate(self.nutritionNeed * time_multiplier)
            if rate * time_multiplier >= self.timeToGrow:
                rate = self.timeToGrow / time_multiplier
            rate = min(rate, 1)
            self.timeToGrow -= rate * time_multiplier
            js[GlobalConfig.global_step_char].append(rate)
        else:
            rate = 0
            js[GlobalConfig.global_step_char].append(0)

        if GlobalConfig.log_growth:
            with open(GlobalConfig.log_path + "/growth.json", "w") as f:
                json.dump(js, f)

        return self.nutritionNeed * time_multiplier * rate

    def full_init(self, args):
        if len(args) == 1:
            args = args[0]
        self.ID = args[0]
        self.growStep = args[1]
        self.absorbRange = args[2]
        self.timeToGrow = args[3]
        self.harvest = args[4]

        self.nutritionNeed.set(list(args[5].dir.values()))

    def get_args(self):
        return self.ID, self.growStep, self.absorbRange, self.timeToGrow, self.harvest, self.nutritionNeed

    def short_init(self, args):
        self = args[2][(args[0], args[1])]

    def __init__(self, *args):
        self.ID = -1
        self.growStep = -1
        self.absorbRange = -1
        self.timeToGrow = -1
        self.harvest = -1
        self.nutritionNeed = NutritionTable()
        if len(args) == 3:
            self.short_init(args)
        elif len(args) != 0:
            self.full_init(args)


def create_plant_list():
    # (id, GrowStep) : Plant(Id,GrowStep,Range,TimeToGrow,Harvest,Nutrition)
    f = open('JsonFiles/PlantList.json')
    p_list = {}
    data = json.load(f)
    for id in data.keys():
        for gs in data[id].keys():
            values = data[id][gs].split(",")
            p_list.update({(int(id), int(gs)): Plant(int(id), int(gs), int(values[0]), float(values[1]),
                                                     float(values[2]),
                                                     NutritionTable(float(values[3]), float(values[4]),
                                                                    float(values[5])))})
    return p_list, len(data.keys())
