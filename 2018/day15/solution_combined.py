import numpy as np
from skimage.graph import MCP
from scipy.spatial.distance import cityblock
import traitlets

DUNGEON = []  # will eventually store the dungeon as numpy array


class Unit(traitlets.HasTraits):
    """
    A generic class to represent units in the dungeon.

    Eeally the only difference is what side the units take, so (just about)
    everything can be defined here.
    """

    attack_power = traitlets.Integer(default_value=3)
    hit_points = traitlets.Integer(default_value=200)

    location = traitlets.Tuple(traitlets.Integer(), traitlets.Integer())  # y, x

    dead = traitlets.Bool(default_value=False)

    members = []  # here to store class instances
    opponents = traitlets.Type('__main__.Unit')

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        cls.members.append(instance)
        return instance

    def attack(self, other):
        other.hit_points -= self.attack_power
        if other.hit_points <= 0:
            other.dead = True
            self.opponents.members.remove(other)

    def distance(self, other):
        return cityblock(self.location, other.location)

    @property
    def target(self):
        """
        Find the nearest target for attack assuming one is available.

        :rtype: Unit
        """
        opponent_distances = [
            self.distance(foe)
            for foe in self.opponents.members
        ]
        potential_targets = [
            foe
            for foe, distance
            in zip(self.opponents.members, opponent_distances)
            if distance == 1
        ]
        if not potential_targets:
            return None
        elif len(potential_targets) == 1:
            return potential_targets[0]
        else:
            return sorted(
                potential_targets,
                key = lambda u: (u.hit_points, *u.location)
            )[0]

    def move(self):
        """
        Move the current unit to the closest valid target

        Use a minimum cost path through the grid, after removing path through
        allies spaces (you can ignore blocking out enemies because if a path
        would go through an enemy it's going to end up closer).

        :rtype: None
        """
        # first, block out your buddies
        current_dungeon = DUNGEON.copy()

        allies = np.array([
            friend.location for friend in self.members
            if friend is not self
        ])

        if allies.size:  # assuming there are any allies left
            # locations are stored as y, x, so:
            current_dungeon[allies[:, 0], allies[:, 1]] = -1

        foe_locations = np.array([
            foe.location
            for foe in self.opponents.members
        ])

        # and now find the costs
        mcp = MCP(current_dungeon, fully_connected=False)
        cum_costs, traceback = mcp.find_costs(
            starts=[self.location],
            find_all_ends=True
        )

        foe_distances = cum_costs[
            foe_locations[:, 0], foe_locations[:, 1]
        ]
        if np.isinf(foe_distances.min()):
            return  # no route available to any foe
        closest_foes = np.arange(len(foe_distances))[foe_distances == foe_distances.min()]
        closest_foe = sorted(
            self.opponents.members[i] for i in
            closest_foes
        )[0]

        # now you have one closest foe, reverse the distance calc
        # and move one step closer

        mcp = MCP(current_dungeon, fully_connected=False)
        cum_costs, traceback = mcp.find_costs(
            ends=[self.location],
            starts=[closest_foe.location],
            find_all_ends=False
        )

        # the minimum foe distance will be the location of self, so decrease
        # by one
        target_locations = np.argwhere(cum_costs == foe_distances.min() - 1)

        # the MCP algorithm will expand out in many directions, so make sure
        # to filter out only those points around self.
        valid_locations = target_locations[(
                (target_locations >= np.array(self.location) - 1) &
                (target_locations <= np.array(self.location) + 1)
        ).all(axis=1)]

        # this is _ugly_, but I couldn't quickly think of a better way to sort
        # the locations
        y, x = (sorted(tuple(coords) for coords in valid_locations))[0]
        self.location = (int(y), int(x))

    # define comparison methods for sorting:
    def __eq__(self, other):
        return self.location == other.location

    def __lt__(self, other):
        return self.location < other.location

    def __gt__(self, other):
        return self.location == other.location

    def __repr__(self):
        """Nice string representation"""
        return f'<{self.__class__.__name__} ap{self.attack_power} hp{self.hit_points} loc{self.location}>'

    # define add and radd so you can easily sum the list of units
    def __add__(self, other):
        return self.hit_points + other.hit_points

    def __radd__(self, other):
        return self.hit_points + other


class Goblin(Unit):
    """A Goblin, sworn enemy of the Christmas Elf"""

    members = []
    # note that using the traitlets type we can defer the dependency on the
    # Elf class until the opponents attribute is accessed
    opponents = traitlets.Type('__main__.Elf')

class Elf(Unit):
    """A Christmas Elf"""

    members = []
    # likewise access to the Goblins is deferred until required.
    opponents = traitlets.Type('__main__.Goblin')

ap = 3  # Elves start with 3 attack points, like goblins
while True:

    # yes, I could change this so that I only created the dungeon object once
    # but really, I figured it would be easier this way
    DUNGEON = []
    Goblin.members.clear()  # make sure the victors are still removed
    Elf.members.clear()

    # create the dungeon from the input file
    for y, line in enumerate(open('input.txt')):

        row = []
        for x, square in enumerate(line.rstrip('\n')):
            if square == '#':
                row.append(-1)
            else:
                row.append(1)
                if square == 'G':
                    Goblin(location=(y, x))  # creating a goblins adds it to the Goblin members
                elif square == 'E':
                    # likewise the elves
                    Elf(location=(y, x), attack_power=ap)
        DUNGEON.append(row)

    DUNGEON = np.array(DUNGEON)

    num_elves = len(Elf.members)  # ensure that no elf dies
    counter = 0
    while Elf.members and Goblin.members:
        for unit in sorted(Goblin.members + Elf.members):
            if not unit.opponents.members or not unit.members:
                break
            if unit.dead:
                continue
            target = unit.target

            if not target:
                unit.move()
                target = unit.target

            if target:
                unit.attack(target)

            if not unit.opponents.members:
                break
        else:
            counter += 1

    if num_elves == len(Elf.members):
        # victory for the elves!
        break
    elif ap == 3:
        print(counter, 'turns')
        print('Solution 1', (counter) * sum(Elf.members + Goblin.members))
    ap += 1

print(ap, 'AP')
print(counter, 'turns')
print('Solution 2', (counter) * sum(Elf.members + Goblin.members))