#!/usr/bin/env python
"""
Solution for day 8 part 1
"""
import io

import numpy as np


def make_image(path: str, cols: int, rows: int) -> np.ndarray:
    """
    Use simple reshaping to make the array
    """
    img = np.loadtxt(path, delimiter=' ', dtype=np.int)
    img = img.reshape(-1, rows, cols)
    return img


def checksum(img: np.ndarray) -> int:
    """
    Find the layer with the minimum number of digits. Multiply the count of 1s on this layer by the number of 2s
    """
    min_zeros_layer = np.argmin(np.sum(img == 0, axis=(1, 2)))
    counts = np.bincount(img[min_zeros_layer].ravel())
    return counts[1] * counts[2]


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
    print(checksum(img))


if __name__ == '__main__':
    main()
