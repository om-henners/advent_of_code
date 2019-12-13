#!/usr/bin/env python
"""
Solution 1 for day 12

Moving around moons
"""
import itertools


class Moon:
    """
    Representation of moons. Should include the ability to time step moons
    """

    _moons = []  # storage for each instance of moons created - populated at init

    def __init__(self, x: int, y: int, z: int, i: int, j: int, k: int):
        self.x = x
        self.y = y
        self.z = z
        self.i = i
        self.j = j
        self.k = k

        self._moons.append(self)

    @classmethod
    def moon_time_zero(cls, x: int, y: int, z: int):
        """
        Shortcut for creating moons at tick zero with zero velocity
        """
        return cls(x, y, z, 0, 0, 0)

    @classmethod
    def clear(cls):
        cls._moons.clear()

    def __repr__(self):
        """
        Easy string representation of the moon as per the problem documentation
        """
        return f"Moon(pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.i}, y={self.j} z={self.k}>"

    @classmethod
    def time_step(cls):
        """
        Advance time for the moons according to the rules in the brief
        """
        # first apply checks for gravity
        for moon_a, moon_b in itertools.combinations(cls._moons, 2):
            if moon_a.x > moon_b.x:
                moon_a.i -= 1
                moon_b.i += 1
            elif moon_a.x < moon_b.x:
                moon_a.i += 1
                moon_b.i -= 1
            if moon_a.y > moon_b.y:
                moon_a.j -= 1
                moon_b.j += 1
            elif moon_a.y < moon_b.y:
                moon_a.j += 1
                moon_b.j -= 1
            if moon_a.z > moon_b.z:
                moon_a.k -= 1
                moon_b.k += 1
            elif moon_a.z < moon_b.z:
                moon_a.k += 1
                moon_b.k -= 1

        for moon in cls._moons:
            moon.x += moon.i
            moon.y += moon.j
            moon.z += moon.k

    @property
    def potential_energy(self):
        """
        Potential energy is the sum of abosolute x, y, z
        """
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self):
        """
        Kinetic iss the sum of absolute i, j, k
        """
        return abs(self.i) + abs(self.j) + abs(self.k)

    @property
    def total_energy(self):
        """
        Total energy is the product of kinetic and potential
        """
        return self.potential_energy * self.kinetic_energy


def main():
    """
    Get the current moon positions after 1000 steps and calculate the energy
    """

    moons = [
        Moon.moon_time_zero(-7, 17, -11),
        Moon.moon_time_zero(9, 12, 5),
        Moon.moon_time_zero(-9, 0, -4),
        Moon.moon_time_zero(4, 6, 0),
    ]

    for _ in range(1000):
        Moon.time_step()

    print(
        sum([moon.total_energy for moon in moons])
    )


if __name__ == '__main__':
    main()
