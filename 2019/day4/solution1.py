#!/usr/bin/env python
"""
However, they do remember a few key facts about the password:

- It is a six-digit number.
- The value is within the range given in your puzzle input.
- Two adjacent digits are the same (like 22 in 122345).
- Going from left to right, the digits never decrease; they only ever
  increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

- 111111 meets these criteria (double 11, never decreases).
- 223450 does not meet these criteria (decreasing pair of digits 50).
- 123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle
input meet these criteria?
"""
from itertools import product
import typing


MIN_PASSWORD = '130254'
MAX_PASSWORD = '678275'


def password_filter(password: str) -> bool:
    """
    Test that the password meets the criteria above
    """

    # happily, strings also work in numeric order in terms of sorting
    if ''.join(sorted(password)) == password and len(set(password)) < len(password):
        return True
    return False


def password_generator() -> typing.Iterator[str]:
    """
    Generator for passwords - uses itertools
    """
    for letters in product('0123456789', repeat=6):
        password = ''.join(letters)
        if password > MIN_PASSWORD and password < MAX_PASSWORD:
            yield password


def main():
    """
    Main work to get the result
    """
    print(sum(1 for _ in filter(password_filter, password_generator())))


if __name__ == '__main__':
    main()
