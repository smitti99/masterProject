import datetime
import json
import logging
import os.path
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy
import numpy as np

import platypus

from EA import EA_Problem, Crossover
from platypus import NSGAII, Problem, Real, DTLZ2, nondominated
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory

import GlobalConfig
from EA.EA_Problem import personal_NSGAII

if __name__ == "__main__":
    base_path = sys.argv[1]
    Logger = logging.getLogger("Platypus")
    log_path = os.path.join(base_path, "EA_Logs.txt")
    if not os.path.exists(log_path):
        with open('/tmp/test', 'w'): pass
    logging.basicConfig(filename=log_path, encoding='utf-8', level=logging.INFO)
    root = tk.Tk()
    root.withdraw()
    file = os.path.join(base_path, 'Nutritions.json')
    with open(file) as f:
        nut = json.load(f)
    timeMult = GlobalConfig.time_mult
    stepNum = GlobalConfig.max_steps

    # define the problem definition
    problem = EA_Problem.Field_Optimization(nut)

    # instantiate the optimization algorithm
    algorithm = personal_NSGAII(problem, population_size=1000, variator=Crossover.row_cross(2))

    print("Starting run at " + str(datetime.datetime.now().time()))
    # optimize the problem using 10,000 function evaluations
    algorithm.log_frequency = 100
    algorithm.run(10000)
    print("finished run at " + str(datetime.datetime.now().time()))
    # display the results

    matplotlib.use('TkAgg')
    fig = plt.figure()

    result = algorithm.result

    ax = fig.add_subplot(projection='3d')
    ax.scatter([s.objectives[0] for s in result],
               [s.objectives[1] for s in result],
               [s.objectives[2] for s in result])
    objectives = []
    for s in nondominated(result):
        objectives.append([s.objectives[0], s.objectives[1], s.objectives[2]])
    print(objectives)
    with open(os.path.join(base_path, "EA-Result.json"), "w") as f:
        json.dump({"result": objectives}, f)
    plt.show()
