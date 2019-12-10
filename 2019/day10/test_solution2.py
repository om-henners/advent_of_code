#!/usr/bin/env python
"""
Tests for solution 2
"""
import io

import numpy as np
import pytest

import solution1
import solution2


@pytest.mark.parametrize(
    'radians, expected',
    [
        (0, 180),
        (np.pi / 2, 90),
        (np.pi, 0),
        (3 * np.pi / 2, 270),
    ]
)
def test_bearings_to_polar_degrees(radians, expected):
    """Make sure my math is good"""
    assert solution2.bearings_to_polar_degrees(radians) == expected


@pytest.fixture(scope='module')
def big_asteroids():
    text = '.#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##'
    asteroids = solution1.read_array(io.StringIO(text))
    return asteroids


@pytest.mark.parametrize(
    'coords, position',
    [
        (np.array([11, 12]), 1),
        (np.array([12, 1]), 2),
        (np.array([12, 2]), 3),
        (np.array([12, 8]), 10),
        (np.array([16, 0]), 20),
        (np.array([16, 9]), 50),
        (np.array([10, 16]), 100),
        (np.array([9, 6]), 199),
        (np.array([8, 2]), 200),
        (np.array([10, 9]), 201),
        (np.array([11, 1]), 299),
    ]
)
def test_orderering(coords, position, big_asteroids):
    """
    Test that for the big asteroids the ordering is correct
    """

    predicted_coords = solution2.order_points_by_angle_distance(big_asteroids)

    assert (predicted_coords[position - 1] == coords).all()


def test_best_position(big_asteroids):
    """
    Just guarnatee that we've got the best position down for the big asteroids
    """
    predicted_coords, predicted_count = solution1.calculate_best_site(big_asteroids)
    assert (predicted_coords == np.array([11, 13])).all()
