from dataclasses import dataclass
from itertools import chain


@dataclass
class Stone:
    engraving: int

    def blink(self) -> list["Stone"]:
        if self.engraving == 0:
            return [Stone(1)]
        text = str(self.engraving)
        if len(text) % 2 == 0:
            left, right = text[: len(text) // 2], text[len(text) // 2 :]
            return [Stone(int(left)), Stone(int(right))]
        return [Stone(self.engraving * 2024)]


data = [Stone(int(val)) for val in open("input").read().strip().split(" ")]

print(data)
for _ in range(25):
    data = chain.from_iterable(stone.blink() for stone in data)
    # data = list(data)
    # print(data)

print(len(list(data)))
