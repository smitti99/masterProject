import datetime
import json

import platypus

from EA import EA_Problem, Crossover
from platypus import NSGAII, Problem, Real, DTLZ2, nondominated
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory

import GlobalConfig

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()
    file = tk.filedialog.askopenfilename(title="Select Nutrition-File")
    with open(file) as f:
        nut = json.load(f)
    timeMult = GlobalConfig.time_mult
    stepNum = GlobalConfig.max_steps

    # define the problem definition
    problem = EA_Problem.Field_Optimization(nut)

    # instantiate the optimization algorithm
    algorithm = NSGAII(problem, population_size=2, variator=Crossover.row_cross)

    print("Starting run at " + str(datetime.datetime.now().time()))
    # optimize the problem using 10,000 function evaluations
    algorithm.run(2)
    print("finished run at " + str(datetime.datetime.now().time()))
    # display the results
    nondominated_solutions = nondominated(algorithm.result)
    for solution in nondominated_solutions:
        print(solution.objectives)
