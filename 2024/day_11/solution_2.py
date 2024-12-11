from functools import cache
from itertools import chain
from typing import Iterator


# @lru_cache(maxsize=10000)
@cache
def blink(engraving: int) -> Iterator[int]:
    if engraving == 0:
        return (1,)

    text = str(engraving)
    if len(text) % 2 == 0:
        left, right = text[: len(text) // 2], text[len(text) // 2 :]
        return (int(left), int(right))

    return (engraving * 2024,)


data = [int(val) for val in open("sample").read().strip().split(" ")]

data = [0]

for _ in range(75):
    data = chain.from_iterable(blink(v) for v in data)

result = list(data)
# print(result)
print(len(result))
