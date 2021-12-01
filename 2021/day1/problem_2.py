"""
Calculate the sliding window sum of each measurement and calculate the number
of times these sums increase.
"""

m1 = [int(l) for l in open('input')]
m2 = m1[1:]
m3 = m2[1:]



previous = [sum(w) for w in zip(m1, m2, m3)]
current = previous[1:]

assert len(m1) == len(previous) + 2, [len(m1), len(previous)]

print(sum(c > p for c, p in zip(current, previous)))
