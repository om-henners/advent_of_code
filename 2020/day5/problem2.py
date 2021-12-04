from itertools import product


chr_map = {ord('F'): ord('0'), ord('B'): ord('1'), ord('L'): ord('0'), ord('R'): ord('1')}

with open('input') as f:
    text = f.read()

numbers = text.translate(chr_map).split()


def get_id(row, col):
    return row * 8 + col


seats = set((get_id(*rc) for rc in product(range(128), range(8))))
passengers = set()

for n in numbers:
    row = int(n[:7], 2)
    col = int(n[7:], 2)

    passengers.add(get_id(row, col))

seats -= passengers


for idx in sorted(seats):
    if idx +1 in passengers and idx -1 in passengers:
        print(idx)
