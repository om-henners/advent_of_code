chr_map = {ord('F'): ord('0'), ord('B'): ord('1'), ord('L'): ord('0'), ord('R'): ord('1')}

with open('input') as f:
    text = f.read()

numbers = text.translate(chr_map).split()

max_id = 0

for n in numbers:
    row = int(n[:7], 2)
    col = int(n[7:], 2)

    new_id = row * 8 + col
    print(row, col, new_id)
    if new_id > max_id:
        max_id = new_id

print(max_id)
