"""
Given some input calculate how many are increasing line by line
"""

current = (int(l) for l in open('input'))
next(current)  # there is no previous value for the first row
previous = (int(l) for l in open('input'))


print(sum(c > p for c, p in zip(current, previous)))
