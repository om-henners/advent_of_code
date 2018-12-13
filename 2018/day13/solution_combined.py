"""
Navigating the cart maze, using a numpy array to represent a maze.

A cart with a centre square X has a value of the sum of the directions that can
be travelled as below:

1   2   4
8   X  16
32 64 128

So, according to the map the directions get numbered as follows:

- => 24
| => 66
/ => 80 or 10
\ => 72 or 18
+ => 90

Other squares will have a value as zero. To check whether a corner is at the
top or bottom of a square we check the current index in the row above
(assuming there is one) - if the value there is 66, then the corder is at the
bottom of square and gets the second value as desceibed above, otherwise it
gets the first. Note, carts can't move diagonally, so the 1, 4, 32 and 128 are
probably superfluous.

If you get a minecart, it is assigned a value as below, and a new minecart is
created at that index:

< or > => 24 (with a direction of 16 and 8 respectively)
^ or V => 66 (with a direction of 64 and 2 respectively)

Note that the direction determines which way the minecart is coming from, and
is used to determine where the cart can go from its current location.
"""
from itertools import cycle
import numpy as np


track_layout = []  # placeholder for what will be a numpy array


class MineCartCollision(Exception):

    def __init__(self, moving_cart, other_cart):
        self.moving_cart = moving_cart
        self.other_cart = other_cart

    def __str__(self):
        return f'Cart {self.moving_cart} hit cart {self.other_cart}'


class Cart:

    all_carts = []

    movement_directions = {
        2: (0, -1),  # note, up is negative y
        8: (-1, 0),  # left is negative x
        16: (1, 0),
        64: (0, 1),
        16 + 64 + 8: [(1, 0), (0, 1), (-1, 0)],  # coming from 2
        2 + 16 + 64: [(0, -1), (1, 0), (0, 1)],  # coming from 8
        64 + 8 + 2: [(0, 1), (-1, 0), (0, -1)],  # coming from 16
        8 + 2 + 16: [(-1, 0), (0, -1), (1, 0)],  # coming from 64
    }
    new_direction = {
        (0, -1): 64,
        (-1, 0): 16,
        (1, 0): 8,
        (0, 1): 2
    }

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.next_turn = cycle([0, 1, 2])
        self.dead = False
        Cart.all_carts.append(self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __repr__(self):
        return f'<Cart {self.x} {self.y} {self.direction}>'

    def tick(self):
        current_location = track_layout[self.y, self.x]
        try:
            movement = self.movement_directions[
                current_location - self.direction
            ]
        except KeyError:
            print(self)
            import matplotlib.pyplot as plt
            plt.imshow(
                track_layout[self.y - 2: self.y + 2, self.x - 2: self.x + 2]
                )
            plt.show()
            raise
        try:
            self.x += movement[0]
            self.y += movement[1]
        except TypeError:
            turn = next(self.next_turn)
            movement = movement[turn]
            self.x += movement[0]
            self.y += movement[1]
        finally:
            self.direction = self.new_direction[movement]

        for cart in Cart.all_carts.copy():  # copy, so on remove don't bork iterator
            if cart is self or cart.dead:
                continue

            if self == cart:
                # remove both carts
                self.dead = True
                cart.dead = True
                Cart.all_carts.remove(self)
                Cart.all_carts.remove(cart)
                raise MineCartCollision(self, cart)


track_values = {
    '-': 24,
    '|': 66,
    '/': (80, 10),
    '\\': (72, 18),
    '+': 90,
    '<': 24,
    '>': 24,
    '^': 66,
    'v': 66,
    ' ': 0,
}
corners = {'/', '\\'}
cart_directions = {
    '<': 16,
    '>': 8,
    '^': 64,
    'v': 2
}


print("Building the minecart track")
for y, line in enumerate(open('input.txt')):
    row = []
    for x, location in enumerate(line.strip('\n')):
        cell_value = track_values[location]
        if location in corners:
            try:
                if track_layout[-1][x] in (66, 90):  # bottom corner
                    cell_value = cell_value[1]
                else:
                    cell_value = cell_value[0]
            except IndexError:
                cell_value = cell_value[0]

        row.append(cell_value)

        try:
            Cart(x, y, cart_directions[location])
        except KeyError:
            pass
    track_layout.append(row)

track_layout = np.array(track_layout)

print(f'Built track {track_layout.shape} and {len(Cart.all_carts)} mine carts')

ticks = 0  # store the number of generations
crash_happened = False
while not crash_happened:

    for cart in sorted(Cart.all_carts):
        if cart.dead:
            continue
        try:
            cart.tick()
        except MineCartCollision as e:  # still want to finish the tick for part 2
            print(e)
            print(f'Solution 1: moving cart location {e.moving_cart}')
            crash_happened = True
    ticks += 1

while len(Cart.all_carts) > 1:

    for cart in sorted(Cart.all_carts):
        if cart.dead:
            continue
        try:
            cart.tick()
        except MineCartCollision as e:  # make sure we get to the end of the tick
            print(e)
    ticks += 1

print(f'Solution 2: Remaining cart {Cart.all_carts[0]}')
