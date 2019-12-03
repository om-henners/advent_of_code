"""Opening the front panel reveals a jumble of wires. Specifically,
two wires are connected to a central port and extend outward on a
grid. You trace the path each wire takes as it leaves the central
port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross
paths. To fix the circuit, you need to find the intersection point
closest to the central port. Because the wires are on a grid, use the
Manhattan distance for this measurement. While the wires do
technically cross right at the central port where they both start,
this point does not count, nor does a wire count as crossing with
itself.
"""
import numpy as np
from shapely import geometry
from scipy.spatial.distance import cdist


def generate_line(wire: str) -> geometry.LineString:
    """Take a string with a direction and a distance and generate a line"""
    line = [[0, 0]]
    for step in wire.split(","):
        direction = step[0]
        distance = int(step[1:])

        vertex = line[-1].copy()
        if direction == "R":
            vertex[0] += distance
        elif direction == "L":
            vertex[0] -= distance
        elif direction == "U":
            vertex[1] += distance
        elif direction == "D":
            vertex[1] -= distance

        line.append(vertex)

    return geometry.LineString(line)


def closest_intersection_distance(wire_1: str, wire_2: str) -> int:
    """Calculate minimum distance to origin point from wire 1 and 2.

    Takes advantage of scipy.spatial.distance.cdist."""
    line_1 = generate_line(wire_1)
    line_2 = generate_line(wire_2)

    points = line_1.intersection(line_2)  # should return a multi-point

    # calc all distances
    distances = cdist([[0, 0]], np.array(points), metric="cityblock")

    # filter out any distances of zero (as the lines will still intersect at the origin point)
    return distances[distances > 0].min().astype(np.int)


def main():
    """Read the data and pass it through to get the question answer"""
    with open('input', 'rt') as directions:
        wires = [line.strip() for line in directions]

    print(closest_intersection_distance(*wires))


if __name__ == '__main__':
    main()
