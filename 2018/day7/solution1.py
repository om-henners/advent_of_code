from parse import parse
import networkx as nx


pattern = 'Step {start} must be finished before step {stop} can begin.'
sleigh_steps = nx.DiGraph()

for line in open('input.txt'):
    result = parse(pattern, line)
    sleigh_steps.add_edge(result['start'], result['stop'])


print(''.join(nx.lexicographical_topological_sort(sleigh_steps)))
# for order in nx.all_topological_sorts(sleigh_steps):
#     print(order)
# print(''.join(min(nx.all_topological_sorts(sleigh_steps))))

import matplotlib.pyplot as plt
pos = nx.nx_agraph.graphviz_layout(sleigh_steps, prog='dot')
nx.draw_networkx(sleigh_steps, pos=pos)
plt.show()
