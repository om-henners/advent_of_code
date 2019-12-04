#!/usr/bin/env python
"""
The two adjacent matching digits are not part of a larger group of matching digits.
"""
from collections import Counter

import solution1


def password_filter(password: str) -> bool:
    """
    Test that the password meets the criteria above
    """
    counts = Counter(password)

    # happily, strings also work in numeric order in terms of sorting
    if ''.join(sorted(password)) == password and len(set(password)) < len(password) and 2 in counts.values():
        return True
    return False


def main():
    """
    Main work to get the result
    """
    print(sum(1 for _ in filter(password_filter, solution1.password_generator())))


if __name__ == '__main__':
    main()
