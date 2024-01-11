import json
import os

import numpy.random

from BaseFunctionality import NutritionTable


def main():
    size = 5
    scale = [40, 25, 75]
    base = [180, 100, 250]
    data = {}
    n = NutritionTable.NutritionTable()
    for i, key in enumerate(n.dir.keys()):
        data.update({key: (numpy.random.normal(0, scale[i], (5, 5)) + base[i]).tolist()})
    with open(os.path.join(os.getcwd(), "JsonFiles", "Nutritions.json"), "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
