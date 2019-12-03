"""
It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:
"""
from shapely import geometry

import solution1


def skip_origin_point(point: geometry.Point) -> bool:
    """Simple filter to trip out any 0, 0 intersection points"""
    return not point.equals(geometry.Point(0, 0))


def minimum_steps(wire_1: str, wire_2: str) -> int:
    """Calculate the minimum number of steps to the intersection point

    Happily we have shapely geometries, so we've got the project method on the lines.
    """
    line_1 = solution1.generate_line(wire_1)
    line_2 = solution1.generate_line(wire_2)

    intersections = line_1.intersection(line_2)

    distances = []
    for point in filter(skip_origin_point, intersections):
        distances.append(line_1.project(point) + line_2.project(point))

    return int(min(distances))


def main():
    """Read the data and pass it through to get the question answer"""
    with open("input", "rt") as directions:
        wires = [line.strip() for line in directions]

    print(minimum_steps(*wires))


if __name__ == "__main__":
    main()
