import numpy as np
from scipy.stats import mode


data = np.array([[int(c) for c in line.strip()] for line in open('input')]).astype(bool)
result, _ = mode(data)

powers = 2 ** np.arange(result.shape[-1] -1, -1, -1)

gamma = powers[result[0]].sum()
epsilon = powers[~result[0]].sum()

print(result)
print(int(''.join(result[0].astype(np.uint0).astype(str)), 2))


print(gamma, epsilon, gamma * epsilon)
