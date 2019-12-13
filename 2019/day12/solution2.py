"""Solution for part 2

Unfortunately I had to look at an explanation here to see that it's
the least common multiple of the periods for each cycle of x, y, z, i,
j, k.
"""
import fractions

import solution1


def lcm(a, b):
    """
    From Rosetta code https://rosettacode.org/wiki/Least_common_multiple#Python
    via https://scicomp.stackexchange.com/a/21235
    """
    return abs(a * b) / fractions.gcd(a, b) if a and b else 0


def main():
    """
    Keep ticking the moons up until they've all cycled at least once
    """

    moons = [
        solution1.Moon.moon_time_zero(-7, 17, -11),
        solution1.Moon.moon_time_zero(9, 12, 5),
        solution1.Moon.moon_time_zero(-9, 0, -4),
        solution1.Moon.moon_time_zero(4, 6, 0),
    ]

    seen_x = set()
    seen_y = set()
    seen_z = set()

    period_x, period_y, period_z = 0, 0, 0

    step = 0

    while True:

        x_pos = tuple((moon.x, moon.i) for moon in moons)
        y_pos = tuple((moon.y, moon.j) for moon in moons)
        z_pos = tuple((moon.z, moon.k) for moon in moons)

        if x_pos in seen_x and not period_x:
            period_x = step

        if y_pos in seen_y and not period_y:
            period_y = step

        if z_pos in seen_z and not period_z:
            period_z = step

        if period_x and period_y and period_z:
            break

        seen_x.add(x_pos)
        seen_y.add(y_pos)
        seen_z.add(z_pos)

        step += 1

        solution1.Moon.time_step()

    print(period_x, period_y, period_z)
    print(lcm(period_x, lcm(period_y, period_z)))


if __name__ == '__main__':
    main()
