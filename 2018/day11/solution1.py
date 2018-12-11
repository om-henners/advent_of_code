import numpy as np
from scipy import ndimage

fuel_cells = np.zeros((300, 300))
x_coord, y_coord = np.meshgrid(np.arange(1, 301), np.arange(1, 301))


rack_id = x_coord + 10
power_level = rack_id * y_coord


SERIAL_NUMBER = 3628
power_level += SERIAL_NUMBER

power_level *= rack_id

power_level = ((power_level // 100) % (power_level // 1000 * 10)) - 5

grid_totals = ndimage.convolve(
    power_level,
#    np.sum,
#    footprint=np.ones((3, 3)),
    weights=np.ones((3, 3)),
    mode='constant',
    cval=0,
    origin=(1, 1)
)


y, x = np.unravel_index(
    np.argmax(grid_totals), (300, 300)
)
print(x+1, y+1)

import matplotlib.pyplot as plt
plt.imshow(grid_totals)
plt.show()
