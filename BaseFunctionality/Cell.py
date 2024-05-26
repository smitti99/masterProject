from BaseFunctionality.NutritionTable import NutritionTable
from BaseFunctionality.Plant import Plant


class Cell:

    def step(self, time_multiplier):
        absorb = self.plant.nutritionNeed * time_multiplier
        if self.plant.timeToGrow <= 0:
            try:
                self.plant = Plant(self.plant_list[(self.plant.ID, self.plant.growStep + 1)].get_args())
            except:
                self.plant.timeToGrow = -1
        unused_nutrition = self.grid.absorb_nutrition(self.position, self.plant.absorbRange, absorb)
        growth = 0
        for key in absorb.dir.keys():
            if ( absorb.dir[key] > 0):
                growth += (absorb.dir[key]-unused_nutrition.dir[key]) / absorb.dir[key]
        growth /= len(absorb.dir.keys())
        self.plant.step(time_multiplier, growth)


    def set_plant(self,plant):
        self.plant = plant

    def set_nutrition(self,nutrition):
        self.nutrition = nutrition
    def __init__(self, x, y, p_list, plant, grid):
        self.plant_list = p_list
        self.position = [x, y]
        self.plant = Plant(plant.get_args())
        self.nutrition = NutritionTable()
        self.grid = grid
