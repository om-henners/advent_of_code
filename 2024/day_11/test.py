import networkx as nx


g = nx.DiGraph()


nx.add_cycle(g, (1, 2, 3))
# nx.add_cycle(g, (1, 2, 1))


def nodes_crossed(dg, start, depth):
    if depth == 0:
        return len(start)

    children = [e[1] for e in dg.out_edges(start)]

    return len(start) + nodes_crossed(dg, children, depth - 1)


print(nodes_crossed(g, [1], 4))
