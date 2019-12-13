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
        solution1.Moon.moon_time_zero(-8, -10, 0),
        solution1.Moon.moon_time_zero(5, 5, 10),
        solution1.Moon.moon_time_zero(2, -7, 3),
        solution1.Moon.moon_time_zero(9, -8, -3),
    ]

    yield m

    solution1.Moon.clear()


@pytest.mark.parametrize(
    "n_steps, expected",
    [
        (
            0,
            [
                (-8, -10, 0, 0, 0, 0),
                (5, 5, 10, 0, 0, 0),
                (2, -7, 3, 0, 0, 0),
                (9, -8, -3, 0, 0, 0),
            ],
        ),
        (
            10,
            [
                (-9, -10, 1, -2, -2, -1),
                (4, 10, 9, -3, 7, -2),
                (8, -10, -3, 5, -1, -2),
                (5, -10, 3, 0, -4, 5),
            ],
        ),
        (
            20,
            [
                (-10, 3, -4, -5, 2, 0),
                (5, -25, 6, 1, 1, -4),
                (13, 1, 1, 5, -2, 2),
                (0, 1, 7, -1, -1, 2),
            ],
        ),
        (
            30,
            [
                (15, -6, -9, -5, 4, 0),
                (-4, -11, 3, -3, -10, 0),
                (0, -1, 11, 7, 4, 3),
                (-3, -2, 5, 1, 2, -3),
            ],
        ),
        (
            40,
            [
                (14, -12, -4, 11, 3, 0),
                (-1, 18, 8, -5, 2, 3),
                (-5, -14, 8, 1, -2, 0),
                (0, -12, -2, -7, -3, -3),
            ],
        ),
        (
            50,
            [
                (-23, 4, 1, -7, -1, 2),
                (20, -31, 13, 5, 3, 4),
                (-4, 6, 1, -1, 1, -3),
                (15, 1, -5, 3, -3, -3),
            ],
        ),
        (
            60,
            [
                (36, -10, 6, 5, 0, 3),
                (-18, 10, 9, -3, -7, 5),
                (8, -12, -3, -2, 1, -7),
                (-18, -8, -2, 0, 6, -1),
            ],
        ),
        (
            70,
            [
                (-33, -6, 5, -5, -4, 7),
                (13, -9, 2, -2, 11, 3),
                (11, -8, 2, 8, -6, -7),
                (17, 3, 1, -1, -1, -3),
            ],
        ),
        (
            80,
            [
                (30, -8, 3, 3, 3, 0),
                (-2, -4, 0, 4, -13, 2),
                (-18, -7, 15, -8, 2, -2),
                (-2, -1, -8, 1, 8, 0),
            ],
        ),
        (
            90,
            [
                (-25, -1, 4, 1, -3, 4),
                (2, -9, 0, -3, 13, -1),
                (32, -8, 14, 5, -4, 6),
                (-1, -2, -8, -3, -6, -9),
            ],
        ),
        (
            100,
            [
                (8, -12, -9, -7, 3, 0),
                (13, 16, -3, 3, -11, -5),
                (-29, -11, -1, -3, 7, 4),
                (16, -13, 23, 7, 1, 1),
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


@pytest.mark.parametrize("n_steps, expected_energy", [(100, 1940)])
def test_calculate_total_energy(n_steps: int, expected_energy: int, moons: Orbit):

    for _ in range(n_steps):
        solution1.Moon.time_step()

    assert sum([moon.total_energy for moon in moons]) == expected_energy
