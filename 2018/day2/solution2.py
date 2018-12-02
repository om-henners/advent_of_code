"""
The boxes will have IDs which differ by exactly one character at the same
position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz

The IDs abcde and axcye are close, but they differ by two characters (the
second and fourth). However, the IDs fghij and fguij differ by exactly one
character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above,
this is found by removing the differing character from either ID, producing
fgij.)
"""
import jellyfish
from scipy.spatial import distance
import numpy as np


levenshtein = np.vectorize(jellyfish.levenshtein_distance)


codes = np.array([word.strip() for word in open('input.txt')])

distances = distance.squareform(
    distance.pdist(codes.reshape(-1, 1), metric=levenshtein)
)
locations = np.unravel_index(
    np.argmin(np.where(distances == 0, np.inf, distances)),
    (len(codes), len(codes))
)
close_words = codes[list(locations)]
same_letters = np.array(list(close_words[0])) == np.array(list(close_words[1]))
print(''.join(np.array(list(close_words[0]))[same_letters]))
