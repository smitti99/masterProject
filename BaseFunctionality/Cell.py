from BaseFunctionality.NutritionTable import NutritionTable
from BaseFunctionality.Plant import Plant


class Cell:

    def step(self, time_multiplier):
        if self.plant.timeToGrow == -1:
            return
        neighbour_nutrition = self.grid.get_neighbour_nutrition(self.position, self.plant.absorbRange)
        absorb = self.plant.step(time_multiplier, neighbour_nutrition)
        if self.plant.timeToGrow <= 0:
            try:
                self.plant = self.plant_list[self.plant.ID, self.plant.growStep + 1]
            except:
                self.plant.timeToGrow = -1
        self.grid.absorb_nutrition(self.position, self.plant.absorbRange, absorb)

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
