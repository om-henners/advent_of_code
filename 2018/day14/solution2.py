import traitlets


PUZZLE_INPUT = [2, 9, 3, 8, 0, 1] # [5, 9, 4, 1, 4] # [5, 1, 5, 8, 9]
RECIPES = [3, 7]


class Elf(traitlets.HasTraits):

    current_location = traitlets.Integer()


    def __add__(self, other):
        return RECIPES[self.current_location] + RECIPES[other.current_location]

    def __radd__(self, other):
        return RECIPES[self.current_location] + other

    def __repr__(self):
        return f'<Elf {self.current_location}>'

    def advance(self):
        self.current_location = (self.current_location + 1 + RECIPES[self.current_location]) % len(RECIPES)


def index(subseq, seq):
    """Return an index of `subseq`uence in the `seq`uence.

    Or `-1` if `subseq` is not a subsequence of the `seq`.

    The time complexity of the algorithm is O(n*m), where

        n, m = len(seq), len(subseq)

    >>> index([1,2], range(5))
    1
    >>> index(range(1, 6), range(5))
    -1
    >>> index(range(5), range(5))
    0
    >>> index([1,2], [0, 1, 0, 1, 2])
    3
    """
    i, n, m = -1, len(seq), len(subseq)
    try:
        while True:
            i = seq.index(subseq[0], i + 1, n - m + 1)
            if subseq == seq[i:i + m]:
               return i
    except ValueError:
        return -1


elves = [Elf(current_location=0), Elf(current_location=1)]

while True:
    current_len = len(RECIPES)
    RECIPES.extend([int(i) for i in str(sum(elves))])
    [e.advance() for e in elves]

    subset = RECIPES[max(current_len - len(PUZZLE_INPUT), 0) :]
    if len(subset) < len(PUZZLE_INPUT):
        continue
    idx = index(PUZZLE_INPUT, subset)
    if idx >= 0:
        print(idx + current_len - len(PUZZLE_INPUT))
        break
    if len(RECIPES) % 1000 == 0:
        print('.', end='')


