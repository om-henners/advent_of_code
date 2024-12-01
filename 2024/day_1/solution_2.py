#!/usr/bin/env python
from collections import Counter

left = []
right = []

with open("input", "rt") as source:
    for line in source.readlines():
        line = line.strip()
        if not line:
            continue
        # print(line)
        l, r = line.split("   ")
        left.append(int(l))
        right.append(int(r))

counter = Counter(right)

similarity = [l * counter.get(l, 0) for l in left]
print(sum(similarity))
