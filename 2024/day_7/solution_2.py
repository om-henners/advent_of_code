from functools import reduce
from itertools import chain, product
from operator import add, mul


data = {
    int(line.strip().split(": ")[0]): [
        int(val) for val in line.strip().split(": ")[1].split(" ")
    ]
    for line in open("input").readlines()
}


def concat(*args):
    return int("".join(str(a) for a in args))


successes = []

for result, calibrators in data.items():
    for ops in chain(
        product(
            [add, mul],
            repeat=len(calibrators) - 1,
        ),
        product([add, mul, concat], repeat=len(calibrators) - 1),
    ):
        iops = iter(ops)

        def apply(a, b):
            op = next(iops)
            return op(a, b)

        if result == reduce(apply, calibrators):
            successes.append(result)
            print(result, ops)
            break

print(sum(successes))
