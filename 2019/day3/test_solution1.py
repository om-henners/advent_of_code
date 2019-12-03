#!/usr/bin/env python
"""
Tests for solution 1
"""
import typing

import pytest
from shapely import geometry

import solution1


@pytest.mark.parametrize(
    "wire_1, wire_2, expected_distance",
    [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 6),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            135,
        ),
    ],
)
def test_closest_intersection_distance(
    wire_1: str, wire_2: str, expected_distance: typing.Union[int, float]
):
    """Test the solutions provided with the question"""
    assert solution1.closest_intersection_distance(wire_1, wire_2) == expected_distance


@pytest.mark.parametrize(
    "wire, expected_length", [("R8,U5,L5,D3", 21), ("U7,R6,D4,L4", 21)]
)
def test_generate_line(wire: str, expected_length: typing.Union[int, float]):
    """Test generating a shapely geometry from the line"""

    line = solution1.generate_line(wire)
    assert isinstance(line, geometry.LineString)
    assert line.length == expected_length
