#!/usr/bin/env python
"""
You are given several natural numbers. Find the longest subsequence that fulfills the following rules.

1. The resulting sequence must be increasing;
2. There cannot be two even numbers together nor two odd numbers together.
"""
sequences = []
sequence = []

for candidate in open('raw').read().split():

    candidate = int(candidate)

    if not sequence or (candidate > sequence[-1] and candidate % 2 != sequence[-1] % 2):
        sequence.append(candidate)
    else:
        sequences.append(sequence)
        sequence = []

else:
    sequences.append(sequence)


print(max(len(sequence) for sequence in sequences))
