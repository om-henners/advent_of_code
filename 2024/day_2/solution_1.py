import csv


reader = csv.reader(open("input"), delimiter=" ")

safe = []
for row in reader:
    row = [int(i) for i in row]
    if not (sorted(row) == row or sorted(row, reverse=True) == row):
        continue

    for left, right in zip(row, row[1:]):
        if not (1 <= abs(right - left) <= 3):
            # print(row)
            break
    else:
        safe.append(row)

print(safe)
print(len(safe))
