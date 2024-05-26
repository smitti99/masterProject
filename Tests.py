from BaseFunctionality.Grid import *


def set_values_test():
    nut = NutritionTable()
    nut.set([1, 2, 3])
    G = Grid()
    G.cells[0][0].nutrition.set([1, 2, 3])
    for key in nut.dir.keys():
        if G.cells[0][0].nutrition.dir[key] != nut.dir[key]:
            raise ValueError("Setting the Nutrition didn't work")
    print("Successfully set Nutritionvalues")


def plant_step_test():
    # Needs to be changed, according to new plant step
    nut = NutritionTable()
    nut.set([4, 5, 6])
    p = Plant(0, 0, 1, 0.5, 1, nut)
    to_absorb = p.step(1, nut)
    for key in to_absorb.dir.keys():
        if to_absorb.dir[key] != nut.dir[key]:
            raise ValueError("Plant Step didn't work")
    print("Plant Step successful")


def absorb_nutrition_test():
    G = Grid()
    for i in range(5):
        for k in range(5):
            G.cells[i][k].nutrition.set([2, 2, 2])
    to_absorb = NutritionTable()
    to_absorb.set([25, 25, 25])
    G.absorb_nutrition((2, 2), 2, to_absorb)
    for i in range(5):
        for k in range(5):
            for key in G.cells[i][k].nutrition.dir.keys():
                if G.cells[i][k].nutrition.dir[key] != 1:
                    raise ValueError("Absorbing Nutrition failed")
    print("Absorb Nutrition successful")


def cell_step_test():
    G = Grid()
    for i in range(5):
        for k in range(5):
            G.cells[i][k].nutrition.set([2, 2, 2])
    nut = NutritionTable()
    nut.set([4.5, 9, 9])
    G.set_cell_data(2, 2, Plant(0, 0, 1, 0.5, 2, nut), None)
    G.cells[2][2].step(1)
    for i in range(1, 4):
        for k in range(1, 4):
            for key in G.cells[i][k].nutrition.dir.keys():
                if (key == "K" and G.cells[i][k].nutrition.dir[key] != 1.5) or \
                        (key != "K" and G.cells[i][k].nutrition.dir[key] != 1):
                    raise ValueError("Cell step failed")
    print("Cell Step successful")


def grid_step_test():
    G = Grid()
    for i in range(5):
        for k in range(5):
            G.set_cell_data(i, k, Plant(0, 0, 1, 5, 1, NutritionTable(0, 0, 0)), NutritionTable(2, 2, 2))
    G.set_cell_data(2, 2, Plant(1, 0, 2, 5, 2, NutritionTable(25, 25, 25)), None)
    G.step(1)
    for i in range(5):
        for k in range(5):
            dictionary = G.cells[i][k].nutrition.dir
            for key in dictionary.keys():
                if dictionary[key] != 1:
                    raise ValueError("Grid step failed")
    print("Grid Step successful")

if __name__ == "__main__":
    set_values_test()
    #plant_step_test()
    absorb_nutrition_test()
    cell_step_test()
    grid_step_test()
