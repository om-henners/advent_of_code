import re

import matplotlib.pyplot as plt
import numpy as np


pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
origin = []
velocity = []
shape = (101, 103)

for line in open("input"):
    m = pattern.match(line)
    if not m:
        continue

    origin.append([m.group(1), m.group(2)])
    velocity.append([m.group(3), m.group(4)])

origin = np.array(origin).astype(int)
velocity = np.array(velocity).astype(int)


seconds = 0
bathroom = np.zeros(shape, dtype=np.int64)

while True:
    destination = origin + velocity * seconds
    # tree = KDTree(destination)

    # near_points = {i for (i, j) in tree.query_pairs(r=1.9) if i != j}
    # if len(near_points) == len(destination):
    #     break

    idx = np.ravel_multi_index(
        (destination[:, 0], destination[:, 1]), bathroom.shape, mode="wrap"
    )

    u_idx, counts = np.unique(idx, return_counts=True, axis=0)
    if np.max(counts) == 1:
        break

    seconds += 1

np.put(bathroom, u_idx, counts, mode="wrap")

print(seconds)

plt.imshow(bathroom.T)
plt.show()
