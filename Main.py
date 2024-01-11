import BaseFunctionality.Display
import GlobalConfig
from BaseFunctionality.Grid import *
from BaseFunctionality.Display import *
from tkinter import Tk
from tkinter.filedialog import askdirectory

verbose = False


def main():
    GlobalConfig.log_path = askdirectory(title='Select Log Folder')
    G = Grid()
    for i in range(5):
        G.step(0.1)
    #show_nutrition(G)
    BaseFunctionality.Display.plot_growth()


if __name__ == "__main__":
    #main()
    #BaseFunctionality.Display.plot_growth()
    BaseFunctionality.Display.plot_yield()
