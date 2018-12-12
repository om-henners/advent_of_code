import numpy as np

generations = 1000
data = open('input.txt')

first_line = data.readline().lstrip('initial state:').strip()
initial_state = [0, 0] * (generations + 1)  # pots preceding zero
for c in first_line:
    if c == '#':
        initial_state.append(1)
    else:
        initial_state.append(0)
initial_state.extend([0, 0] * (generations + 1))  # empty trailing pots
inital_state = np.array(initial_state, dtype=np.bool)

data.readline()  # skip blank line

matchers = []
response = []
for line in data:
    pattern, res = line.strip().split(' => ')
    match = []
    for c in pattern:
        if c == '#':
            match.append(1)
        else:
            match.append(0)
    matchers.append(match)
    if res == '#':
        response.append(1)
    elif res == '.':
        response.append(0)
    else:
        raise ValueError('Matching failed')

matchers = np.array(matchers, dtype=np.bool)
response = np.array(response, dtype=np.bool)

# print(matchers.shape)
# print(initial_state)
idxs = np.arange(len(initial_state)) - 2 * (generations + 1)

generation_sums = []

for i in range(generations):
    new_state = [False, False]
    for j in range(2, len(initial_state) - 3):
        candidate = initial_state[j-2: j+3]

        new_state.append(response[(matchers == candidate).all(axis=1)])
    new_state.extend([False, False, False])
    initial_state = np.hstack(new_state)
    generation_sums.append(idxs[initial_state].sum())

# import matplotlib.pyplot as plt
# plt.plot(generation_sums)
# plt.show()

print(generation_sums[[150, 200, 300, 400]])
