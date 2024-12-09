from collections import deque
from itertools import batched, repeat


disk = deque()

for file_id, b in enumerate(batched(open("input").read().strip(), n=2)):
    print(b)

    disk.extend(repeat(file_id, int(b[0])))

    if len(b) > 1:
        disk.extend(repeat(None, int(b[1])))


repack = []


while disk:
    data = disk.popleft()

    if data is None:
        disk.rotate()
    else:
        repack.append(data)

# print(repack)

checksum = [i * v for i, v in enumerate(repack)]
print(sum(checksum))
