import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


lines = np.loadtxt("input", dtype=str)
data = lines.view("U1").reshape((lines.size, -1))

target = np.array(["M", "A", "S"])


count = 0

# search rows and columns
windows = sliding_window_view(data, window_shape=(len(target), len(target)))

left = windows.diagonal(axis1=-2, axis2=-1)
right = windows[:, :, ::-1].diagonal(axis1=-2, axis2=-1)

a = np.sum(np.all((left == target) & (right == target), axis=-1))
b = np.sum(np.all((left == target[::-1]) & (right == target), axis=-1))
c = np.sum(np.all((left == target[::-1]) & (right == target[::-1]), axis=-1))
d = np.sum(np.all((left == target) & (right == target[::-1]), axis=-1))
print(a + b + c + d)
