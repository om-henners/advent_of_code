from collections import deque
from itertools import product

import networkx as nx
import numpy as np


depth = 6084
target = 14, 709  # x, y
# Test
# depth = 510
# target = 10, 10


geological_index = np.zeros((target[1] * 2, target[0] * 2))
erosion_level = np.zeros((target[1] * 2, target[0] * 2))

x_coords, y_coords = np.meshgrid(np.arange(target[0] * 2), np.arange(target[1] * 2))

geological_index[y_coords == 0] = x_coords[y_coords == 0] * 16807
geological_index[x_coords == 0] = y_coords[x_coords == 0] * 48271
erosion_level[y_coords == 0] = (geological_index[y_coords == 0] + depth) % 20183
erosion_level[x_coords == 0] = (geological_index[x_coords == 0] + depth) % 20183


dependencies = nx.DiGraph()
for y, x in product(range(0, target[1] * 2), range(0, target[0] * 2)):
    if y > 0:
        dependencies.add_edge((y - 1, x), (y, x))
    if x > 0:
        dependencies.add_edge((y, x - 1), (y, x))

stack = deque()
for node in nx.topological_sort(dependencies):
    stack.appendleft(node)
    if 0 in node:
        continue

    geological_index[node[0], node[1]] = erosion_level[node[0] - 1, node[1]] * erosion_level[node[0], node[1] -1]
    erosion_level[node[0], node[1]] = (geological_index[node[0], node[1]] + depth) % 20183

geological_index[target[1], target[0]] = geological_index[0, 0]
erosion_level[target[1], target[0]] = erosion_level[0, 0]

terrain = (erosion_level % 3).astype(np.int)

acceptable_carries = {
    0: {'climbing gear', 'torch'},    # rock
    1: {'climbing gear', 'neither'},  # wet
    2: {'torch', 'neither'}           # narrow
}

path_grid = nx.grid_2d_graph(*terrain.shape, create_using=nx.DiGraph)
while stack:
    y, x = stack.pop()

    if (y, x) == (0, 0):
        path_grid.node[(y, x)].update({'total_cost': 0, 'equipment': 'torch'})
        continue

    surrounding_nodes = filter(
        lambda n: -1 not in n and 'total_cost' in path_grid.node[n],
        [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]
    )

    possible_sources = {}
    for source in surrounding_nodes:
        if path_grid.node[source]['equipment'] in acceptable_carries[terrain[y, x]]:
            possible_sources[source] = {'cost': 1, 'equipment': path_grid.node[source]['equipment']}
        else:
            possible_sources[source] = {
                'cost': 8,
                'equipment': (acceptable_carries[terrain[y, x]] & acceptable_carries[terrain[source[0], source[1]]]).pop()
            }





# import matplotlib.pyplot as plt
# plt.imshow(terrain)
# plt.show()
