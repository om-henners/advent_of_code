#!/usr/bin/env python
"""
Tests for day 8 part 1
"""
import io
import pytest

import numpy as np

import solution1


@pytest.mark.parametrize(
    "numbers, cols, rows, expected",
    [
        ('123456789012', 3, 2, np.array([[[1, 2, 3],[4,5,6]],[[7,8,9],[0,1,2]]]))
    ]
)
def test_make_image(numbers, cols, rows, expected):

    text = io.StringIO(' '.join(numbers))
    text.seek(0)

    assert (solution1.make_image(text, cols, rows) == expected).all()


@pytest.mark.parametrize(
    "numbers, cols, rows, expected",
    [
        ('123456789012', 3, 2, 1)
    ]
)
def test_checksum(numbers, cols, rows, expected):
    text = io.StringIO(' '.join(numbers))
    text.seek(0)

    img = solution1.make_image(text, cols, rows)

    assert solution1.checksum(img) == expected
