from collections import defaultdict
from itertools import cycle

import numba
import numpy as np
from scipy import ndimage

PLAYERS = 468
LAST_MARBLE = 7184300

SCORES = defaultdict(int)


@numba.jit(nopython=True)
def sped_up_marbles():

    circle = [0, ]
    current_idx = 0

    current_player = 0
    scores = np.zeros(PLAYERS, dtype=np.uint64)

    for i in range(1, LAST_MARBLE + 1):

        if i % 23 == 0:
            scores[current_player] += i
            current_idx = (current_idx - 7) % len(circle)
            scores[current_player] += circle.pop(current_idx)
        else:
            target_idx = (current_idx + 2) % len(circle)
            if target_idx == 0:
                target_idx = len(circle)
            circle.insert(target_idx, i)
            current_idx = target_idx

        current_player = (current_player + 1) % PLAYERS

    return scores

print(sped_up_marbles().max())

# data = np.array(list(sped_up_marbles()))
# print(data.shape)

# print(ndimage.sum(data[:, 1], data[:, 0], np.unique(data[:, 0])).max())

# for player, score in sped_up_marbles():
#     SCORES[player] += score


# print(max(SCORES.values()))
