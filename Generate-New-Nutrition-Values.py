import json
import os

import numpy.random

from BaseFunctionality import NutritionTable


def main():
    size = 5
    dev = [10, 4, 10]
    mean = [20, 6, 20]
    data = {}
    n = NutritionTable.NutritionTable()
    for i, key in enumerate(n.dir.keys()):
        array = numpy.random.normal(mean[i], dev[i], (size, size))
        array[array < 0] = 0
        data.update({key: array.tolist()})
    with open(os.path.join(os.getcwd(), "JsonFiles", "Nutritions.json"), "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
