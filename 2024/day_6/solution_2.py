from collections import deque

import numpy as np
from skimage.morphology import dilation
from skimage.segmentation import flood_fill


def calculate_route(museum, start):
    structure = np.array([[0, 1, 0], [0, 1, 0], [0, 0, 0]], dtype=np.uint8)
    direction = deque([1, 2, 4, 8])

    route = np.zeros(museum.shape, dtype=np.uint8)

    while True:
        # museum_with_stops = dilation(museum, structure).astype(np.uint8) - museum
        path = (
            flood_fill(museum, start, direction[0], footprint=structure).astype(
                np.uint8
            )
            - museum
        )
        if np.any(np.bitwise_and(route, path)):
            raise OverflowError("Found a loop")

        route = np.bitwise_or(route, path)

        stop = path * dilation(museum, structure).astype(np.uint8)

        if not np.any(stop):
            break
        start = next(zip(*np.where(stop)))

        structure = np.rot90(structure, k=-1)
        direction.rotate(-1)
    return route


lines = np.loadtxt("input", dtype=str, comments=None)
data = lines.view("U1").reshape((lines.size, -1))

museum = np.zeros(data.shape, dtype=np.uint8)
museum[data == "#"] = 16

# start = tuple(int(ij) for ij in np.where(data == "^"))
start = next(zip(*np.where(data == "^")))
print("start", start)


original_route = calculate_route(museum, start)

rows, cols = np.where(original_route)

block_counts = 0

for row, col in zip(rows, cols):
    if (row, col) == start:
        # print("skipping start")
        continue

    blocked = np.copy(museum)
    blocked[row, col] = 16

    try:
        calculate_route(blocked, start)
    except OverflowError:
        print(row, col)
        block_counts += 1


print(block_counts)
