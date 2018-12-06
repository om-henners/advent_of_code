import numpy as np
from scipy.spatial import distance

# read the data using scipy
points = np.loadtxt('input.txt', delimiter=', ')

# build a grid of the appropriate size - note the + 1 to ensure all points
# are within the grid
xmin, ymin = points.min(axis=0) - 1
xmax, ymax = points.max(axis=0) + 2

# and use mesgrid to build the target coordinates
xgrid, ygrid = np.meshgrid(np.arange(xmin, xmax), np.arange(xmin, xmax))
targets = np.dstack([xgrid, ygrid]).reshape(-1, 2)

# happily scipy.spatial.distance has cityblock (or manhatten) distance out
# of the box
cityblock = distance.cdist(points, targets, metric='cityblock')
# the resulting array is an input points x target points array
# so get the index of the maximum along axis 0 to tie each target coordinate
# to closest ID
closest_origin = np.argmin(cityblock, axis=0)
# we need to filter out points with competing closest IDs though
min_distances = np.min(cityblock, axis=0)
competing_locations_filter = (cityblock == min_distances).sum(axis=0) > 1
# note, integers in numpy don't support NaN, so make the ID higher than
# the possible point ID
closest_origin[competing_locations_filter] = len(points) + 1
# and those points around the edge of the region for "infinite" regions
closest_origin = closest_origin.reshape(xgrid.shape)
print(closest_origin)
infinite_ids = np.unique(np.vstack([
    closest_origin[0],
    closest_origin[-1],
    closest_origin[:, 0],
    closest_origin[:, -1]
]))
closest_origin[np.isin(closest_origin, infinite_ids)] = len(points) + 1

# and because we know the id of the "null" data is guaranteed to be last
# in the array (it's highest) we can index it out before getting the max
# region size
print(np.max(np.bincount(closest_origin.ravel())[:-1]))

# finally, make a pretty picture for good measure
import matplotlib.pyplot as plt
plt.imshow(np.where(closest_origin > len(points), np.NaN, closest_origin))
plt.colorbar()
plt.show()
