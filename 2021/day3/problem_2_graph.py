"""Graph in the form a -> b

Where edge is the count of ones or zeros and the node is the value (1 or 0), and to keep the levels unique the level number.
"""
import networkx as nx


g = nx.DiGraph()


# first populate the graph

for line in open('input'):
    line = line.strip()

    for level, (start, end) in enumerate(zip(line, line[1:5])):

        n1 = line[:level]
        n2 = line[:level + 1]

        if g.has_edge(n1, n2):
            g.edges[n1, n2]["count"] += 1

        else:
            g.add_edge(n1, n2, count=1)


import matplotlib.pyplot as plt

pos = nx.planar_layout(g)
nx.draw_networkx(g, pos=pos)
plt.show()
