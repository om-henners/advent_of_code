import numpy as np


snowfield = np.array([
    [0 if c == '.' else 1 for c in line.strip()]
    for line in open('input')
])

trees = []

for right_step, down_step in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    row_idx = np.arange(0, snowfield.shape[0], down_step)
    col_idx = (np.arange(len(row_idx)) * right_step) % snowfield.shape[1]

    num_trees = snowfield[row_idx, col_idx].sum()
    print(num_trees)
    trees.append(num_trees)

print(np.prod(trees))
