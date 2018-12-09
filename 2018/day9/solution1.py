from collections import defaultdict
from itertools import cycle

PLAYERS = 468
LAST_MARBLE = 71843

SCORES = defaultdict(int)


circle = [0, ]
current_idx = 0

# print(circle)

for i, player in zip(range(1, LAST_MARBLE + 1), cycle(range(PLAYERS))):
    if i % 100000 == 0:
        print('.', end='')

    if i % 23 == 0:
        SCORES[player] += i
        current_idx = (current_idx - 7) % len(circle)
        SCORES[player] += circle.pop(current_idx)
    else:
        target_idx = (current_idx + 2) % len(circle)
        if target_idx == 0:
            target_idx = len(circle)
        circle.insert(target_idx, i)
        current_idx = target_idx
    # print(circle)

print(max(SCORES.values()))
