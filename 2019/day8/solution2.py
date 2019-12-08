#!/usr/bin/env python
"""
Solution for day 8 part 1
"""
import io

import matplotlib.pyplot as plt
import numpy as np


def make_image(path: str, cols: int, rows: int) -> np.ndarray:
    """
    Use simple reshaping to make the array
    """
    img = np.loadtxt(path, delimiter=' ', dtype=np.int)
    img = img.reshape(-1, rows, cols)
    return img


def first_number(a: np.ndarray) -> int:
    """
    """
    mask = a != 2
    return a[mask][0]


def collapse_message(img: np.ndarray):
    """
    Set 2 pixels to empty and get the first value underneath
    """
    message = np.apply_along_axis(first_number, 0, img)

    plt.imshow(message)
    plt.show()


def main():
    """
    Main runner
    """
    img = make_image(
        io.StringIO(
            ' '.join(open('input').read().strip())
        ),
        25,
        6
    )
    collapse_message(img)


if __name__ == '__main__':
    main()
