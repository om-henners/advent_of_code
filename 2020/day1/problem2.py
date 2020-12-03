from itertools import product

numbers = [int(n) for n in open('input')]


for a, b, c in product(
        filter(lambda n: n < 1000, numbers),
        numbers,
        numbers
):
    if a + b + c == 2020:
        print(a, b, c, a*b*c)
        break
