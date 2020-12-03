from itertools import product

numbers = [int(n) for n in open('input')]


for a, b in product(
        filter(lambda n: n < 1000, numbers),
        numbers):
    if a + b == 2020:
        print(a, b, a*b)
        break
