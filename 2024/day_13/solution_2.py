from sympy import solve, Integer
from sympy.abc import a, b
import textfsm


template = textfsm.TextFSM(open("template"))
machines = template.ParseText(open("input").read())


def is_whole_token(root: dict) -> bool:
    return isinstance(root[a], Integer) and isinstance(root[b], Integer)


def cost(root: dict) -> Integer:
    return root[a] * 3 + root[b]


costs = []

for machine in machines:
    xs, ys, end_x, end_y = machine

    eq_x = a * int(xs[0]) + b * int(xs[1]) - int(end_x) - 10000000000000
    eq_y = a * int(ys[0]) + b * int(ys[1]) - int(end_y) - 10000000000000

    roots = solve([eq_x, eq_y], a, b, dict=True)
    roots = filter(is_whole_token, roots)

    try:
        costs.append(cost(min(roots, key=cost)))
    except ValueError:
        pass

print(sum(costs))
