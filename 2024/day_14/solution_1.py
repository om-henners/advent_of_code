import re

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

# initial state
# points, counts = np.unique(origin, return_counts=True, axis=0)
# bathroom = np.zeros((11, 7))
# np.put(
#     bathroom,
#     np.ravel_multi_index((points[:, 0], points[:, 1]), bathroom.shape, mode='wrap'),
#     counts,
#     mode='wrap'
# )
# print(bathroom.T)


# # print(origin)
bathroom = np.zeros(shape, dtype=np.int64)
destination = origin + velocity * 100
print(destination)
idx = np.ravel_multi_index(
    (destination[:, 0], destination[:, 1]), bathroom.shape, mode="wrap"
)

u_idx, counts = np.unique(idx, return_counts=True, axis=0)
np.put(bathroom, u_idx, counts, mode="wrap")
print(bathroom.T)

ul = bathroom[
    : np.floor(bathroom.shape[0] / 2).astype(int),
    : np.floor(bathroom.shape[1] / 2).astype(int),
].sum()
ur = bathroom[
    : np.floor(bathroom.shape[0] / 2).astype(int),
    np.ceil(bathroom.shape[1] / 2).astype(int) :,
].sum()
ll = bathroom[
    np.ceil(bathroom.shape[0] / 2).astype(int) :,
    : np.floor(bathroom.shape[1] / 2).astype(int),
].sum()
lr = bathroom[
    np.ceil(bathroom.shape[0] / 2).astype(int) :,
    np.ceil(bathroom.shape[1] / 2).astype(int) :,
].sum()
print(ul, ur, ll, lr)
print(ul * ur * ll * lr)
