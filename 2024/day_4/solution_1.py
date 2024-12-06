import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


lines = np.loadtxt("input", dtype=str)
data = lines.view("U1").reshape((lines.size, -1))

print(data.shape)

target = np.array(["X", "M", "A", "S"])


count = 0

# search rows and columns
for axis in (0, 1):
    windows = sliding_window_view(data, window_shape=len(target), axis=axis)

    count += np.sum(np.all(windows == target, axis=-1))
    count += np.sum(np.all(windows == target[::-1], axis=-1))

    print(count)

# print(windows)
# print(windows == target)
# print(np.all(windows == target, axis=-1))

#

# print(count)

for arr in (data, data[::-1, :]):
    rows, cols = arr.shape

    for i in range(-rows, cols + 1):
        #        print(arr.diagonal(i))

        diag = arr.diagonal(i)
        print("".join(diag))
        if len(diag) < len(target):
            continue

        windows = sliding_window_view(diag, window_shape=len(target))

        count += np.sum(np.all(windows == target, axis=-1))
        count += np.sum(np.all(windows == target[::-1], axis=-1))

print(count)
