import numba
import numpy as np
from scipy.ndimage import generic_filter


@numba.jit(nopython=True)
def state_change(data):
    """
    Generic filter for changing the state of trees

    Data comes in as a flattened array of:

    a b c
    d e f
    g h i

    So, current contents is index 3, or data[4]

    Assume data is recorded with the values described in the puzzle replaced by integers

    - 1 for open ground
    - 2 for trees
    - 3 for a lumberyard
    """

    if data[4] == 0:
        if np.sum(data == 1) >= 3:
            return 1
        else:
            return 0
    if data[4] == 1:
        if np.sum(data == 2) >= 3:
            return 2
        else:
            return 1
    if data[4] == 2:
        if np.sum(data == 2) >= 2 and np.sum(data == 1) >= 1:
            return 2
        else:
            return 0


def generate_result(state):
    return np.sum(state == 1) * np.sum(state == 2)


datamap = {'.': 0, '|': 1, '#': 2}
data = np.array([
    [datamap[c] for c in line.strip()]
    for line in open('input.txt')
])

STEPS = 10000 # 10
for i in range(STEPS):
    data = generic_filter(data, state_change, size=3, mode='constant', cval=0)

print('Solution 1', generate_result(data))