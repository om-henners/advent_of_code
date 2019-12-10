#!/usr/bin/env python
"""
Tests for solution 1
"""
import io

import numpy as np
import pytest

import solution1


@pytest.mark.parametrize(
    "txt",
    [
        ".#..#\n.....\n#####\n....#\n...##\n",
        "......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####\n",
        "#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.\n",
        ".#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..\n",
        ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##\n",
    ],
)
def test_read_array(txt):
    """tests the read array function to ensure it returns an array of boolean values"""

    asteroids = solution1.read_array(io.StringIO(txt))

    assert isinstance(asteroids, np.ndarray)
    assert asteroids.ndim == 2


@pytest.mark.parametrize(
    "txt",
    [
        ".#..#\n.....\n#####\n....#\n...##\n",
        "......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####\n",
        "#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.\n",
        ".#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..\n",
        ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##\n",
    ],
)
def test_coordinate_generation(txt):
    """Tests the coordate generation by counting the coordinate pairs generated"""

    asteroids = solution1.read_array(io.StringIO(txt))

    assert len(solution1.coordinate_generation(asteroids)) == np.sum(asteroids)


@pytest.mark.parametrize(
    "coords, expected",
    [
        (np.array([[0, 0], [0, 0]]), 0),
        (np.array([[0, 0], [1, 0]]), np.pi / 2),
        (np.array([[0, 0], [0, 1]]), 0),
        (np.array([[0, 0], [1, 1]]), np.pi / 4),
        (np.array([[0, 0], [-1, 0]]), -np.pi / 2),
        (np.array([[0, 0], [0, -1]]), np.pi),
    ],
)
def test_bearing_generation(coords: np.ndarray, expected: float):
    """
    Trick for this problem is to count the number of identical bearings for each row, so bearing generation is the important bit
    """
    distances = solution1.bearing(coords)
    assert distances[0, 1] == expected


@pytest.mark.parametrize(
    "txt, expected_coords, expected_count",
    [
        (".#..#\n.....\n#####\n....#\n...##\n", (3, 4), 8),
        (
            "......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####\n",
            (5, 8),
            33,
        ),
        (
            "#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.\n",
            (1, 2),
            35,
        ),
        (
            ".#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..\n",
            (6, 3),
            41,
        ),
        (
            ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##\n",
            (11, 13),
            210,
        ),
    ],
)
def test_best_site(txt, expected_coords, expected_count):
    """
    Test against examples in the brief
    """

    asteroids = solution1.read_array(io.StringIO(txt))

    predicted_coords, predicted_count = solution1.calculate_best_site(asteroids)

    assert predicted_count == expected_count
    assert (predicted_coords == np.array(expected_coords)).all()
