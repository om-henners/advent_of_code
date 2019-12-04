"""
Tests for solution 2 for day 4 of the puzzle
"""
import pytest

import solution2


@pytest.mark.parametrize(
    "password, passes",
    [("112233", True), ("123444", False), ("111122", True)],
)
def test_password_filter(password: str, passes: bool):
    """Test the passwords correctly pass or fail the filter"""
    assert solution2.password_filter(password) == passes
