import copy
import random

import numpy
from platypus import Problem, Integer, Real, Variator


class random_crossover(Variator):

    def __init__(self):
        super().__init__(2)

    def evolve(self, parents):
        child1 = copy.deepcopy(parents[0])
        child2 = copy.deepcopy(parents[1])

        nvars = child1.problem.nvars

        for i in range(nvars):
            if random.uniform(0.0, 1.0) <= 0.5:
                child1.variables[i] = parents[1].variables[i]
                child2.variables[i] = parents[0].variables[i]

        return [child1, child2]


class row_cross(Variator):

    def __init__(self):
        super().__init__(2)

    def evolve(self, parents):
        child1 = copy.deepcopy(parents[0])
        child2 = copy.deepcopy(parents[1])

        nvars = child1.problem.nvars
        rows = numpy.sqrt(nvars - 3)
        row1 = numpy.random.randint(0, rows)
        row2 = numpy.random.randint(0, rows)
        child1.variables[rows * row1:rows * (row1 + 1)] = parents[1].variables[rows * row2:rows * (row2 + 1)]
        child2.variables[rows * row2:rows * (row2 + 1)] = parents[0].variables[rows * row1:rows * (row1 + 1)]

        return [child1, child2]

class col_cross(Variator):

    def __init__(self):
        super().__init__(2)

    def evolve(self, parents):
        child1 = copy.deepcopy(parents[0])
        child2 = copy.deepcopy(parents[1])

        nvars = child1.problem.nvars
        col = numpy.sqrt(nvars - 3)
        col1 = numpy.random.randint(0, col)
        col2 = numpy.random.randint(0, col)
        for i in range(col):
            child1.variables[col1 + i*col] = parents[1].variables[col2 + i*col]
            child2.variables[col2 + i*col] = parents[0].variables[col1 + i*col]

        return [child1, child2]
