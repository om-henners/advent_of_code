#!/usr/bin/env python
"""
Test for solution 1
"""
from typing import List, Tuple, Iterator

import pytest

import solution1


Orbit = List[solution1.Moon]


@pytest.fixture()
def moons() -> Iterator[Orbit]:
    """
    Create moons for testing
    """

    m = [
        solution1.Moon.moon_time_zero(-1, 0, 2),
        solution1.Moon.moon_time_zero(2, -10, -7),
        solution1.Moon.moon_time_zero(4, -8, 8),
        solution1.Moon.moon_time_zero(3, 5, -1),
    ]

    yield m

    solution1.Moon.clear()


@pytest.mark.parametrize(
    "n_steps, expected",
    [
        (
            0,
            [
                (-1, 0, 2, 0, 0, 0),
                (2, -10, -7, 0, 0, 0),
                (4, -8, 8, 0, 0, 0),
                (3, 5, -1, 0, 0, 0),
            ],
        ),
        (
            1,
            [
                (2, -1, 1, 3, -1, -1),
                (3, -7, -4, 1, 3, 3),
                (1, -7, 5, -3, 1, -3),
                (2, 2, 0, -1, -3, 1),
            ],
        ),
        (
            2,
            [
                (5, -3, -1, 3, -2, -2),
                (1, -2, 2, -2, 5, 6),
                (1, -4, -1, 0, 3, -6),
                (1, -4, 2, -1, -6, 2),
            ],
        ),
        (
            3,
            [
                (5, -6, -1, 0, -3, 0),
                (0, 0, 6, -1, 2, 4),
                (2, 1, -5, 1, 5, -4),
                (1, -8, 2, 0, -4, 0),
            ],
        ),
        (
            4,
            [
                (2, -8, 0, -3, -2, 1),
                (2, 1, 7, 2, 1, 1),
                (2, 3, -6, 0, 2, -1),
                (2, -9, 1, 1, -1, -1),
            ],
        ),
        (
            5,
            [
                (-1, -9, 2, -3, -1, 2),
                (4, 1, 5, 2, 0, -2),
                (2, 2, -4, 0, -1, 2),
                (3, -7, -1, 1, 2, -2),
            ],
        ),
        (
            6,
            [
                (-1, -7, 3, 0, 2, 1),
                (3, 0, 0, -1, -1, -5),
                (3, -2, 1, 1, -4, 5),
                (3, -4, -2, 0, 3, -1),
            ],
        ),
        (
            7,
            [
                (2, -2, 1, 3, 5, -2),
                (1, -4, -4, -2, -4, -4),
                (3, -7, 5, 0, -5, 4),
                (2, 0, 0, -1, 4, 2),
            ],
        ),
        (
            8,
            [
                (5, 2, -2, 3, 4, -3),
                (2, -7, -5, 1, -3, -1),
                (0, -9, 6, -3, -2, 1),
                (1, 1, 3, -1, 1, 3),
            ],
        ),
        (
            9,
            [
                (5, 3, -4, 0, 1, -2),
                (2, -9, -3, 0, -2, 2),
                (0, -8, 4, 0, 1, -2),
                (1, 1, 5, 0, 0, 2),
            ],
        ),
        (
            10,
            [
                (2, 1, -3, -3, -2, 1),
                (1, -8, 0, -1, 1, 3),
                (3, -6, 1, 3, 2, -3),
                (2, 0, 4, 1, -1, -1),
            ],
        ),
    ],
)
def test_position_after_n_steps(n_steps: int, expected: List[Tuple[int]], moons: Orbit):
    """
    Test the position and velocity of the moons at some particular step
    """
    for _ in range(n_steps):
        solution1.Moon.time_step()

    for candidate, moon in zip(expected, moons):
        assert (moon.x, moon.y, moon.z, moon.i, moon.j, moon.k) == candidate


@pytest.mark.parametrize(
    'n_steps, expected_energy',
    [
        (10, 179)
    ]
)
def test_calculate_total_energy(n_steps: int, expected_energy: int, moons: Orbit):

    for _ in range(n_steps):
        solution1.Moon.time_step()

    assert sum([moon.total_energy for moon in moons]) == expected_energy
