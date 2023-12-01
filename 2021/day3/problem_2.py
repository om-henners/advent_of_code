import numpy as np
from scipy.stats import mode


data = np.array([[int(c) for c in line.strip()] for line in open('input')]).astype(bool)


def most_common(rows):
    if rows.size == 0:
        return ''

    column = rows[:, 0]

    zero, one = np.bincount(column)

    if zero > one:
        return '0' + most_common(rows[column == 0, 1:])
    else:
        return '1' + most_common(rows[column == 1, 1:])


def least_common(rows):
    if rows.size == 0:
        return ''

    column = rows[:, 0]

    zero, one = np.bincount(column)

    if one > zero:
        return '0' + least_common(rows[column == 0, 1:])
    else:
        return '1' + least_common(rows[column == 1, 1:])


most = most_common(data)
least = least_common(data)


print(most, int(most, 2), least, int(least, 2), int(most, 2) * int(least, 2))
