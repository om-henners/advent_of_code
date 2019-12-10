#!/usr/bin/env python
"""
Solution for part 1

Find the best location for the asteroid base
"""
import typing

import numpy as np


def bearing(coords: np.ndarray) -> np.ndarray:
    """
    Return angle between points in radians
    """
    xs = coords[:, 0] - coords[:, 0].reshape(-1, 1)
    ys = coords[:, 1] - coords[:, 1].reshape(-1, 1)
    distances = np.arctan2(xs, ys)
    return np.where(np.eye(len(distances)), np.nan, distances)


def read_array(file: typing.TextIO) -> np.ndarray:
    """
    Process the data from the file like object into a numpy ndarray
    """
    array = np.array([
        list(line.strip())
        for line
        in file
    ])

    return array == '#'


def coordinate_generation(array: np.ndarray) -> np.ndarray:
    """
    Use numpy's nonzero and column stack to get the array of coordinats
    """
    locations = np.nonzero(array)
    return np.column_stack(locations[::-1])  # coordinats are xy, not yx


def count_uniques(row):
    """
    Count the unique values in row -1 (becase nan counts as a unique value)
    """
    return len(np.unique(row)) - 1


def calculate_best_site(asteroids):
    """
    Calculate the best site by calculating all the angles, and summing the unique values returned.

    The poisition of the max will give you back the correct coordinate as well.
    """
    coords = coordinate_generation(asteroids)

    distances = bearing(coords)

    # will have the same length and order as coords
    unique_counts = np.apply_along_axis(count_uniques, 0, distances)

    highest_count = unique_counts.max()
    best_position = coords[np.argmax(unique_counts)]

    return best_position, highest_count


def main():
    """
    Open the input, get it read and get the answer
    """
    with open('input') as f:
        asteroids = read_array(f)

    best_position, highest_count = calculate_best_site(asteroids)
    print(best_position, highest_count)


if __name__ == '__main__':
    main()
