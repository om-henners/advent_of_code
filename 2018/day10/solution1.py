import numpy as np
from parse import parse


starts = []
increments = []

for line in open('input.txt'):
    r = parse('position=<{x:6d}, {y:6d}> velocity=<{xi:2d}, {yi:2d}>\n', line)
    if not r:
        raise ValueError(f'Could not parse "{line}"')
    starts.append([r['x'], r['y']])
    increments.append([r['xi'], r['yi']])


starts = np.array(starts)
increments = np.array(increments)


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

starts += increments * 10639

fig, ax = plt.subplots()
scat = ax.scatter(starts[:, 0], starts[:, 1])# , origin='upper')
ax.invert_yaxis()
# plt.show( )
plt.show()

def update(i):
    scat.set_offsets(starts + increments * i)

animation = FuncAnimation(fig, update, np.arange(20), interval=1000)
plt.show()

# area = (starts[:, 1].max() - starts[:, 1].min())
# print(area)

# i = 0
# while starts[:, 1].min() < -200:
#     i += 1
#     starts += increments * i
#     # new_area = (starts.max(axis=0) - starts.min(axis=0)).prod()
#     area = (starts[:, 1].max() - starts[:, 1].min())

# print(area)
# starts -= increments

# fig, ax = plt.subplots()
# scat = ax.scatter(starts[:, 0], starts[:, 1])# , origin='upper')
# ax.invert_yaxis()
# plt.show()
# print(i)
