from NutritionTable import NutritionTable


class Plant:
    ID = -1
    growStep = -1
    absorbRange = -1
    timeToGrow = -1
    harvest = -1
    nutritionNeed = NutritionTable()

    def step(self, timeMultiplier, Nutritions):
        rate = Nutritions.get_min_rate(self.nutritionNeed * timeMultiplier)
        if rate > 1:
            rate = 1
        self.timeToGrow -= rate
        return self.nutritionNeed * timeMultiplier * rate
