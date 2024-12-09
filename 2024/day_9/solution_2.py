from dataclasses import dataclass
from itertools import chain

from collections import deque
from itertools import batched


@dataclass
class Block:
    id: int | None
    size: int
    start: int

    def overwrite(self, other: "Block") -> None:
        if self.id is not None:
            raise ValueError("Can't overwrite free space")
        if other.id is None:
            raise ValueError("Can't overwrite with free space")
        if other.size > self.size:
            raise ValueError("Block too small")

        other.start = self.start

        self.size -= other.size
        self.start += other.size

    @property
    def checksum(self) -> int:
        if self.id is None:
            return 0

        return sum(self.id * i for i in range(self.start, self.start + self.size))


disk = deque()

start = 0

for file_id, b in enumerate(batched(open("input").read().strip(), n=2)):
    disk.append(Block(file_id, int(b[0]), start))
    start += disk[-1].size

    if len(b) > 1:
        disk.append(Block(None, int(b[1]), start))
        start += disk[-1].size

repack = []

while disk:
    print(len(disk), len(repack))
    block = disk.popleft()

    if block.id is not None:
        repack.append(block)
        continue

    failed = []
    print("Free space to fill:", block)

    while disk:
        candidate = disk.pop()
        try:
            block.overwrite(candidate)
            # print("\tSuccess:", candidate, block)
            repack.append(candidate)
            failed.append(block)
            break
        except ValueError:
            failed.append(candidate)
            # print("\tFailed:", candidate)
    else:
        # print("No candidates")
        repack.append(block)

    disk = deque(
        sorted((b for b in chain(disk, failed) if b.size > 0), key=lambda b: b.start)
    )


print(sum(b.checksum for b in repack))

# print(repack)

# checksum = [
#     i * v for i, v in enumerate(repack)
# ]
# print(sum(checksum))
