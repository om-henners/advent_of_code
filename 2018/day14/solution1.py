import traitlets


PUZZLE_INPUT = 293801
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


elves = [Elf(current_location=0), Elf(current_location=1)]

while len(RECIPES) <= PUZZLE_INPUT + 10:
    RECIPES.extend([int(i) for i in str(sum(elves))])
    [e.advance() for e in elves]

print(''.join(str(i) for i in RECIPES[PUZZLE_INPUT: PUZZLE_INPUT + 10]))