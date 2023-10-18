import matplotlib
from BaseFunctionality.NutritionTable import *
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
