import json
import os

import matplotlib
import numpy

from BaseFunctionality.NutritionTable import *
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog

import threading


def pause_and_wait():
    input("Press Enter to continue...")


def show_nutrition(Grid):
    matplotlib.use('TkAgg')
    x_size = len(Grid.cells)
    y_size = len(Grid.cells[0])
    keys = NutritionTable().dir.keys()
    data = {}
    for key in keys:
        data.update({key: [[0.0 for i in range(y_size)] for k in range(x_size)]})
    for x in range(x_size):
        for y in range(y_size):
            cell_data = Grid.cells[x][y].nutrition.dir
            for key in keys:
                data[key][x][y] = cell_data[key]
    fig_lis = []
    for key in keys:
        f, a = plt.subplots(figsize=(15, 15))
        a.set_title(key)
        a.imshow(np.array(data[key]), cmap='RdYlGn')
        f.show()
        fig_lis.append(f)
        plt.pause(1)
    pause_thread = threading.Thread(target=pause_and_wait)
    pause_thread.start()
    while pause_thread.is_alive():
        plt.pause(1)
    pause_thread.join()
    for fig in fig_lis:
        plt.close(fig)


def plot_growth():
    try:
        matplotlib.use('TkAgg')
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename(title="Select Growth-Log")
        with open(file) as f:
            in_data = json.load(f)
            plot_data = []
            for key in in_data.keys():
                plot_data.append(numpy.average(in_data[key]))
            fig, axs = plt.subplots()
            axs.set_ylabel("Average-Growth-Rate")
            axs.set_xlabel("Step")
            axs.set_ylim([0,1])
            axs.plot(plot_data)
            fig.savefig(os.path.join(os.path.dirname(file), "growth_plot"))
    except Exception as e:
        print(e)
        print("No Logs found / Wrong File selected")


def plot_yield():
    try:
        matplotlib.use('TkAgg')
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename(title="Select Yield-Log")
        with open(file) as f:
            in_data = json.load(f)
            plot_data = []
            for key in in_data.keys():
                plot_data.append(numpy.average(in_data[key]))
            fig, axs = plt.subplots()
            axs.set_ylabel("Average-Yield-Rate")
            axs.set_xlabel("Step")
            axs.plot(plot_data)
            fig.savefig(os.path.join(os.path.dirname(file), "yield_plot"))
    except Exception as e:
        print(e)
        print("No Logs found / Wrong File selected")

