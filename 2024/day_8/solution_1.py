from itertools import chain, permutations

import string

import numpy as np


lines = np.loadtxt("sample", dtype=str)
data = lines.view("U1").reshape((lines.size, -1))


points = []

for freq in chain(string.ascii_lowercase, string.ascii_uppercase, string.digits):
    rows, cols = np.where(data == freq)
    if not len(rows):
        continue

    for left, right in permutations(zip(rows, cols), 2):
        left, right = sorted((left, right))

        left, right = np.array(left), np.array(right)

        d_row_col = right - left
        # print(d_row, d_col)

        points.append(left - d_row_col)
        points.append(right + d_row_col)
        # print(left, right, *points[-2:])


points = np.array(points)

mask = (
    (points[:, 0] >= 0)
    & (points[:, 0] < data.shape[0])
    & (points[:, 1] >= 0)
    & (points[:, 1] < data.shape[1])
)


points = np.unique(points[mask], axis=0)

# print(len(points))


antinodes = np.zeros(data.shape, dtype=np.uint16)
antinodes[points[:, 0], points[:, 1]] = 1
# antinodes[data != '.'] = 0

print(antinodes)

print(np.sum(antinodes))
