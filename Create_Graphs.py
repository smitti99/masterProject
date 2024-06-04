import os
import tkinter as tk
from tkinter import filedialog
import json

import matplotlib
import matplotlib.pyplot as plt

import numpy


def Epoch_Logs(file):
    with open(os.path.join(file, "Epoch_Logs.json")) as f:
        epoch_logs = json.load(f)
    x = []
    o1 = []
    o2 = []
    o3 = []
    for epoch in epoch_logs.keys():
        x.append(int(epoch))
        avg = numpy.average(epoch_logs[epoch], axis=0)
        minim = numpy.min(epoch_logs[epoch], axis=0)
        maxim = numpy.max(epoch_logs[epoch], axis=0)
        o1.append([maxim[0], avg[0], minim[0]])
        o2.append([maxim[1], avg[1], minim[1]])
        o3.append([maxim[2], avg[2], minim[2]])

    matplotlib.use('TkAgg')
    fig, axs = plt.subplots()
    axs.plot(x, o1)
    axs.set_xlabel("Generation")
    axs.set_ylabel("Yield")
    axs.legend(["Max", "Avg", "Min"])
    plt.savefig(os.path.join(file, "Yield_plot.png"))
    plt.cla()
    axs.plot(x, o2)
    axs.set_xlabel("Generation")
    axs.set_ylabel("Nut_Error")
    axs.legend(["Max", "Avg", "Min"])
    plt.savefig(os.path.join(file, "Nut_plot.png"))
    plt.cla()
    axs.plot(x, o3)
    axs.set_xlabel("Generation")
    axs.set_ylabel("Fert_Cost")
    axs.legend(["Max", "Avg", "Min"])
    plt.savefig(os.path.join(file, "Fert_plot.png"))


def result_logs(file):
    with open(os.path.join(file, "EA-Result.json")) as f:
        logs = json.load(f)
    o1 = []
    o2 = []
    o3 = []
    for indiv in logs.values():
        o1.append(indiv[0][0])
        o2.append(indiv[0][1])
        o3.append(indiv[0][2])
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    ax1.set_xlabel("Yield")
    ax1.set_ylabel("Nut_Error")
    ax1.scatter(o1,o2)
    ax2.set_xlabel("Yield")
    ax2.set_ylabel("Fert_Cost")
    ax2.scatter(o1, o3)
    ax3.set_xlabel("Fert_Cost")
    ax3.set_ylabel("Nut_Error")
    ax3.scatter(o3, o2)
    plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file = tk.filedialog.askdirectory()
    Epoch_Logs(file)
    result_logs(file)
