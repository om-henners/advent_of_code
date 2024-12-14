import numpy as np
from rasterio import features
from shapely import geometry
from skimage.measure import label


lines = np.loadtxt("input", dtype=str)
data = lines.view("U1").reshape((lines.size, -1))
data = data.view(np.int32)

# print(data.dtype)
# print(label(data))


geoms = [
    geometry.shape(poly)
    for poly, label in features.shapes(label(data).astype(np.int32))
]


costs = []

for poly in geoms:
    edge_count = sum(
        [len(poly.exterior.coords) - 1, *(len(i.coords) - 1 for i in poly.interiors)]
    )
    costs.append(edge_count * poly.area)

print(costs)
print(sum(costs))
