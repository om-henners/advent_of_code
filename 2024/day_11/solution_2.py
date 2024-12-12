from functools import cache


@cache
def blink(engraving: int, depth: int) -> int:
    if depth == 0:
        return 1  # stone

    if engraving == 0:
        return blink(1, depth - 1)

    text = str(engraving)
    if len(text) % 2 == 0:
        left, right = text[: len(text) // 2], text[len(text) // 2 :]
        return blink(int(left), depth - 1) + blink(int(right), depth - 1)

    return blink(engraving * 2024, depth - 1)


data = map(int, open("input").read().split())

print(sum(blink(val, 75) for val in data))
# 236804088748754
