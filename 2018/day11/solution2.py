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

max_power = 0
y = x = 0
best_i = 0
print("Starting checks")
for i in range(1, 301):

    print(i)

    # grid_totals = ndimage.generic_filter(
    #     power_level,
    #     np.sum,
    #     size=i,
    grid_totals = ndimage.convolve(
        power_level,
        weights=np.ones((i, i)),
        mode='constant',
        cval=0,
    )

    candidate = grid_totals.max()
    if candidate > max_power:
        max_power = candidate

        y, x = np.unravel_index(
            np.argmax(grid_totals), (300, 300)
        )
        best_i = i
        print(x+1 - i // 2, y+1 - i // 2, best_i)


print(x+1 - i // 2, y+1 - i // 2, best_i)


# import matplotlib.pyplot as plt
# plt.imshow(grid_totals)
# plt.show()
