import numpy as np
from scipy import ndimage

spring = (0, 500)  # y, x

data = []
coords = {'x': [spring[1] ], 'y': [spring[0] ]}  # include the spring location

for line in open('input.txt'):

    row = {}

    for half in line.strip().split(', '):
        nums = [int(i) for i in half[2:].split('..')]
        try:
            row[half[0]] = slice(nums[0], nums[1] + 1)
        except IndexError:
            row[half[0]] = nums[0]

        coords[half[0]].extend(nums)

    data.append(row)


scan = np.ones(
    (max(coords['y']) + 2, max(coords['x']) + 2),
    dtype=np.uint
)


for row in data:
    scan[row['y'], row['x']] = 0

scan = scan[:, min(coords['x']):]
spring = (0, 500 - min(coords['x']))


x_open_spaces = np.vstack((
    ndimage.label(row)[0] for row in scan
))
y_open_spaces = np.column_stack((
    ndimage.label(row)[0] for row in scan.T
))


x_coords = np.arange(scan.shape[1])
y_coords = np.arange(scan.shape[0])


drop = y_open_spaces[spring[0]] == y_open_spaces[spring[0], spring[1]]






import matplotlib.pyplot as plt
plt.figure(figsize=(5, 20))
plt.imshow(y_open_spaces, cmap='gist_rainbow', interpolation='nearest')
plt.imshow(np.where(scan==0, 0, np.NaN), cmap='gray')
plt.scatter(*spring[::-1], color='black', marker='s')
plt.savefig('wells.png')