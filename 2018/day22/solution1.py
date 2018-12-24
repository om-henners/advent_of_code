from itertools import product

import networkx as nx
import numpy as np


depth = 6084
target = 14, 709  # x, y
# Test
# depth = 510
# target = 10, 10


geological_index = np.zeros((target[1] + 1, target[0] + 1))
erosion_level = np.zeros((target[1] + 1, target[0] + 1))

x_coords, y_coords = np.meshgrid(np.arange(target[0] + 1), np.arange(target[1] + 1))

geological_index[y_coords == 0] = x_coords[y_coords == 0] * 16807
geological_index[x_coords == 0] = y_coords[x_coords == 0] * 48271
erosion_level[y_coords == 0] = (geological_index[y_coords == 0] + depth) % 20183
erosion_level[x_coords == 0] = (geological_index[x_coords == 0] + depth) % 20183


dependencies = nx.DiGraph()
for y, x in product(range(1, target[1] + 1), range(1, target[0] + 1)):
    dependencies.add_edge((y - 1, x), (y, x))
    dependencies.add_edge((y, x - 1), (y, x))

for node in nx.topological_sort(dependencies):
    if 0 in node:
        continue

    geological_index[node[0], node[1]] = erosion_level[node[0] - 1, node[1]] * erosion_level[node[0], node[1] -1]
    erosion_level[node[0], node[1]] = (geological_index[node[0], node[1]] + depth) % 20183

geological_index[target[1], target[0]] = geological_index[0, 0]
erosion_level[target[1], target[0]] = erosion_level[0, 0]

terrain = erosion_level % 3
print(terrain.sum())

import matplotlib.pyplot as plt
plt.imshow(terrain)
plt.show()