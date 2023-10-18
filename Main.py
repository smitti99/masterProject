from BaseFunctionality.Grid import *
from BaseFunctionality.Display import *


def main():
    G = Grid()
    for i in range(5):
        G.step(0.1)
    show_nutrition(G)


if __name__ == "__main__":
    main()
