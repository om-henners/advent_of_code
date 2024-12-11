from itertools import product

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


lines = np.loadtxt("input", dtype=str)
data = lines.view("U1").reshape((lines.size, -1)).astype(int)


starts = []
ends = []

mountain = nx.DiGraph()

col_diff = np.diff(data, axis=1)

# left to right
rows, cols = np.where(col_diff == 1)
mountain.add_edges_from(zip(zip(rows, cols), zip(rows, cols + 1)))
# right to left
rows, cols = np.where(col_diff == -1)
mountain.add_edges_from(zip(zip(rows, cols + 1), zip(rows, cols)))


row_diff = np.diff(data, axis=0)
print(row_diff)
# north to south
rows, cols = np.where(row_diff == 1)
mountain.add_edges_from(zip(zip(rows, cols), zip(rows + 1, cols)))
# south to north
rows, cols = np.where(row_diff == -1)
mountain.add_edges_from(zip(zip(rows + 1, cols), zip(rows, cols)))


starts = zip(*np.where(data == 0))
ends = zip(*np.where(data == 9))

routes = {}

for start, end in product(starts, ends):
    try:
        nx.shortest_path(mountain, start, end)
    except nx.NetworkXNoPath:
        pass
    else:
        routes[start] = routes.get(start, 0) + 1

print(sum(routes.values()))

mountain = nx.relabel_nodes(
    mountain, {n: (int(n[0]), int(n[1])) for n in mountain.nodes}
)

pos = {n: (n[1], len(data) - n[0]) for n in mountain.nodes}

nx.draw_networkx(mountain, pos=pos)
plt.show()
