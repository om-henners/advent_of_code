"""
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a
single square inch of fabric with any other claim. If you can somehow draw
attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are
made.

What is the ID of the only claim that doesn't overlap?
"""
import numpy as np
import parse

claim_matcher = '''#{id:d} @ {x:d},{y:d}: {width:d}x{height:d}\n'''
fabric = np.zeros((1000, 1000), dtype=np.int)


for line in open('input.txt'):
    r = parse.parse(claim_matcher, line)
    claim = fabric[r['y']: r['y'] + r['height'], r['x']: r['x'] + r['width']]
    claim[:] = claim + 1


for line in open('input.txt'):
    r = parse.parse(claim_matcher, line)
    claim = fabric[r['y']: r['y'] + r['height'], r['x']: r['x'] + r['width']]

    if claim.max() == 1:
        print(r['id'])
