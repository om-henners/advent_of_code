#!/usr/bin/env python
"""
Solution for part 2

Findd the 200th asteroid to be exploded
"""
import typing

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

import solution1


def bearings_to_polar_degrees(distances: np.ndarray) -> np.ndarray:
    """
    Go from radians in standard cartesian coordinates degrees in polar north coordinates
    """
    return np.degrees(np.pi - distances) % 360


def sort_by_distance(origin: np.ndarray, coords: np.ndarray) -> np.ndarray:
    """
    Get points from coordinates sorted by distance from origin
    """
    distances = cdist([origin], coords)[0]  # only going to be one origin
    idx = np.argsort(distances)
    return idx


def order_points_by_angle_distance(asteroids):
    """
    Get the best location. Then order all points by angle and distance for the destruction of astroids
    """
    coords = solution1.coordinate_generation(asteroids)

    bearings = solution1.bearing(coords)

    # Will have the same length and order as coords
    unique_counts = np.apply_along_axis(solution1.count_uniques, 0, bearings)

    best_position = coords[np.argmax(unique_counts)]
    best_point_bearings = bearings_to_polar_degrees(
        bearings[np.argmax(unique_counts)]
    )

    # separate points from other points
    other_points = np.ones(len(coords)).astype(np.bool)
    other_points[np.argmax(unique_counts)] = False
    other_coords = coords[other_points]
    other_bearings = best_point_bearings[other_points]

    distance_ranks = np.ones(len(other_coords))
    for bear in np.unique(other_bearings):
        distance_ranks[other_bearings == bear] = sort_by_distance(
            best_position,
            other_coords[other_bearings == bear]
        )

    idx = np.arange(len(other_coords))
    idx = sorted(idx, key=lambda i: (distance_ranks[i], other_bearings[i]))
    sorted_coords = other_coords[idx]

    return sorted_coords


def main():
    """
    Open the input, get it read and get the answer
    """
    with open('input') as f:
        asteroids = solution1.read_array(f)

    print(order_points_by_angle_distance(asteroids)[199])


if __name__ == '__main__':
    main()
