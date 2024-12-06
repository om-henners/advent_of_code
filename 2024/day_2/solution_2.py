import csv


def is_safe(row):
    if not (sorted(row) == row or sorted(row, reverse=True) == row):
        return False

    for left, right in zip(row, row[1:]):
        if not (1 <= abs(right - left) <= 3):
            return False
    return True


reader = csv.reader(open("input"), delimiter=" ")

safe = []
for row in reader:
    row = [int(i) for i in row]

    if is_safe(row):
        safe.append(row)
        continue
    for i in range(len(row)):
        if is_safe(row[:i] + row[i + 1 :]):
            safe.append(row)
            break

print(safe)
print(len(safe))
