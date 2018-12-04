"""
If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)
"""
import parse
import pandas as pd

# 1: sort input (text sort should work)
# 2: Use pandas to build a Series for each guard on a particular day - should
#    have 1 of 3 vals: NaN for not present, 1 for asleep, 0 for awake
# 3: Build dataframe with a datetime index, and with column indexes being the guard ID
# 4: sums across two axis, and idxmax.

data = sorted(open('input.txt').readlines())
print(len(data))
print(data[:5])
