import numpy as np


snowfield = np.array([
    [0 if c == '.' else 1 for c in line.strip()]
    for line in open('input')
])

col_idx = (np.arange(snowfield.shape[0]) * 3) % snowfield.shape[1]
print(snowfield[np.arange(snowfield.shape[0]), col_idx].sum())
