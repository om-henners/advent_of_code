#!/usr/bin/env python


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


diff = [abs(r - l) for l, r in zip(sorted(left), sorted(right))]
print(sum(diff))
