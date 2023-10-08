from NutritionTable import NutritionTable


class Plant:
    ID = -1
    growStep = -1
    absorbRange = -1
    timeToGrow = -1
    harvest = -1
    nutritionNeed = NutritionTable()

    def step(self, time_multiplier, nutritions):
        rate = nutritions.get_min_rate(self.nutritionNeed * time_multiplier)
        if rate > 1:
            rate = 1
        self.timeToGrow -= rate
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
    p_list = {(0, 0): Plant(0, 0, 1, 1, 5, NutritionTable(1, 1, 1)),
              (1, 1): Plant(0, 1, 1, 1, 1, NutritionTable(2, 2, 2))}

    return p_list, 1
