import copy
import datetime
import gc
import logging
import random
import time
#from tkinter.filedialog import askdirectory

from platypus import Problem, Integer, Real, NSGAII, RandomGenerator, TournamentSelector, MaxEvaluations, \
    TerminationCondition, nondominated

import GlobalConfig
from BaseFunctionality import Plant, Grid, NutritionTable, HelperFunctions


class Field_Optimization(Problem):

    def __init__(self, Nutrition):

        super().__init__(28, 3)
        self.types[0:25] = Integer(0, 3)
        self.types[25:] = Real(0, 2)
        self.directions[1:] = Problem.MINIMIZE
        self.directions[0] = Problem.MAXIMIZE
        self.nutrition = Nutrition
        GlobalConfig.log_nutrition = False
        GlobalConfig.log_yield = False
        GlobalConfig.log_growth = False

    def evaluate(self, solution):
        # exract plants from variables
        plant_list = Plant.create_plant_list()
        plants_index = solution.variables[:25]
        plants = [[plant_list[0][(0, 0)] for y in range(5)] for x in range(5)]
        for x in range(5):
            for y in range(5):
                plants[x][y] = plant_list[0][(plants_index[x * 5 + y], 0)]

        # setup grid for simulation
        grid_nutrition = HelperFunctions.convert_nutrition_array(self.nutrition)
        g = Grid.Grid(grid_nutrition, plants)
        g.l_nutrition = False
        g.l_yield = False
        # extract fertilizer from variables
        fertilizer_list = solution.variables[25:]
        fertilizer = NutritionTable.NutritionTable(fertilizer_list[0], fertilizer_list[1], fertilizer_list[2])
        g.fertilizer = fertilizer
        g.to_fertilize = True

        # simulate
        for i in range(GlobalConfig.max_steps):
            g.step(GlobalConfig.time_mult)

        # evaluate
        nutrition_error = 0
        plant_yield = 0
        for x in range(5):
            for y in range(5):
                plant_yield += g.cells[x][y].plant.harvest
                nutrition_error += HelperFunctions.evaluate_nutrition_value(g.cells[x][y].nutrition)

        plant_yield /= 25
        nutrition_error /= 25
        cost = HelperFunctions.nutrition_to_cost(g.fertilizer) * 25 * GlobalConfig.max_steps

        solution.objectives[:] = [plant_yield, nutrition_error, cost]
        del g
        gc.collect()


class personal_NSGAII(NSGAII):
    def __init__(self, problem,
                 population_size=100,
                 generator=RandomGenerator(),
                 selector=TournamentSelector(2),
                 variator=None,
                 archive=None,
                 **kwargs):
        super().__init__(problem, population_size, generator, selector, variator, archive, **kwargs)

    def run(self, condition, callback=None):
        LOGGER = logging.getLogger("Platypus")
        if isinstance(condition, int):
            condition = MaxEvaluations(condition)

        if isinstance(condition, TerminationCondition):
            condition.initialize(self)

        last_log = self.nfe
        start_time = time.time()

        LOGGER.log(logging.INFO, "%s starting", type(self).__name__)

        while not condition(self):
            self.step()
            if self.log_frequency is not None and self.nfe >= last_log + self.log_frequency:
                nondominated_solutions = nondominated(self.result)
                out = str(self.nfe)+" "
                for solution in nondominated_solutions:
                    out += str(solution.objectives)+";"
                LOGGER.log(logging.INFO, out)
                last_log = self.nfe

            if callback is not None:
                callback(self)
            self.nfe += 1

        LOGGER.log(logging.INFO,
                   "%s finished; Total NFE: %d, Elapsed Time: %s",
                   type(self).__name__,
                   self.nfe,
                   datetime.timedelta(seconds=time.time() - start_time))
