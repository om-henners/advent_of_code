import numpy as np
from skimage.morphology import dilation
from skimage.segmentation import flood_fill


lines = np.loadtxt("input", dtype=str, comments=None)
data = lines.view("U1").reshape((lines.size, -1))

structure = np.array([[0, 1, 0], [0, 1, 0], [0, 0, 0]], dtype=np.uint8)

museum = np.zeros(data.shape, dtype=np.uint8)
museum[data == "#"] = 2

start = tuple(int(ij) for ij in np.where(data == "^"))
print(start)

route = np.zeros(data.shape, dtype=np.uint8)

while True:
    # museum_with_stops = dilation(museum, structure).astype(np.uint8) - museum
    path = flood_fill(museum, start, 1, footprint=structure).astype(np.uint8) - museum
    route += path

    stop = path * dilation(museum, structure).astype(np.uint8)
    if not np.any(stop):
        break
    start = tuple(int(ij) for ij in np.where(stop))
    structure = np.rot90(structure, k=-1)


print(route)
print(np.sum(route > 0))
