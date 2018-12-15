import matplotlib.pyplot as plt
import numpy as np
from skimage.graph import MCP
from scipy.spatial.distance import cityblock
import traitlets


DUNGEON = []


class Unit(traitlets.HasTraits):

    attack_power = traitlets.Integer(default_value=3)
    hit_points = traitlets.Integer(default_value=200)

    location = traitlets.Tuple(traitlets.Integer(), traitlets.Integer())  # y, x

    dead = traitlets.Bool(default_value=False)

    members = []
    opponents = traitlets.Type('__main__.Unit')

    @classmethod
    def append(cls, other):
        cls.members.append(other)

    def attack(self, other):
        other.hit_points -= self.attack_power
        if other.hit_points <= 0:
            other.dead = True
            self.opponents.members.remove(other)
            print(self, 'killed', other)

    def distance(self, other):
        return cityblock(self.location, other.location)

    @property
    def target(self):
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
        # first, block out your buddies
        current_dungeon = DUNGEON.copy()

        allies = np.array([
            friend.location for friend in self.members
            if friend is not self
        ])

        if allies.size:
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
            #ends=foe_locations,
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

        target_locations = np.argwhere(cum_costs == foe_distances.min() - 1)
        valid_locations = target_locations[(
                (target_locations >= np.array(self.location) - 1) &
                (target_locations <= np.array(self.location) + 1)
        ).all(axis=1)]
        if valid_locations.size == 0:
            print(valid_locations)

        y, x = (sorted(tuple(coords) for coords in valid_locations))[0]
        print(self, 'moving to', y, x)
        self.location = (int(y), int(x))


    def __eq__(self, other):
        return (*self.location, self.hit_points) == (*other.location, other.hit_points)

    def __lt__(self, other):
        return (*self.location, self.hit_points) < (*other.location, other.hit_points)

    def __gt__(self, other):
        return (*self.location, self.hit_points) == (*other.location, other.hit_points)

    def __repr__(self):
        return f'<{self.__class__.__name__} ap{self.attack_power} hp{self.hit_points} loc{self.location}>'

    def __add__(self, other):
        return self.hit_points + other.hit_points

    def __radd__(self, other):
        return self.hit_points + other


class Goblin(Unit):

    members = []
    opponents = traitlets.Type('__main__.Elf')

class Elf(Unit):

    members = []
    opponents = traitlets.Type('__main__.Goblin')

ap = 4
while True:
    DUNGEON = []
    Goblin.members.clear()
    Elf.members.clear()

    print("Set up and populate the dungeon")
    for y, line in enumerate(open('input.txt')):

        row = []
        for x, square in enumerate(line.rstrip('\n')):
            if square == '#':
                row.append(-1)
            else:
                row.append(1)
                if square == 'G':
                    Goblin.append(Goblin(location=(y, x)))
                elif square == 'E':
                    Elf.append(Elf(location=(y, x), attack_power=ap))
        DUNGEON.append(row)

    DUNGEON = np.array(DUNGEON)
    print("Dungeon dungeon'd")

    num_elves = len(Elf.members)
    counter = 0
    while Elf.members and Goblin.members:
        print('Turn', counter)
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
        break
    else:
        ap += 1


print(ap, 'AP')
print(counter, 'turns')
print(Elf.members + Goblin.members)
print(sum(Elf.members + Goblin.members))
print((counter) * sum(Elf.members + Goblin.members))