"""
Tests for solution 1 for day 4 of the puzzle
"""
import pytest

import solution1


@pytest.mark.parametrize(
    "password, passes",
    [("122345", True), ("111111", True), ("223450", False), ("123789", False)],
)
def test_password_filter(password: str, passes: bool):
    """Test the passwords correctly pass or fail the filter"""
    assert solution1.password_filter(password) == passes


def test_password_generator():
    """Test that the password generator gets passwords correctly"""
    for candidate in solution1.password_generator():
        assert isinstance(candidate, str)
        assert len(candidate) == 6
        assert candidate > solution1.MIN_PASSWORD and candidate < solution1.MAX_PASSWORD
