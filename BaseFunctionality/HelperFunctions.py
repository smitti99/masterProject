def avg(values):
    sum = 0.0
    count = 0.0
    for value in values:
        sum += value
        count += 1
    return sum / count


def min(values):
    min = values[0]
    for value in values:
        if value < min:
            min = value
    return min
