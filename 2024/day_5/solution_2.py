import networkx as nx


g = nx.DiGraph()

with open("input") as f:
    lines = iter(f.readlines())

    for line in lines:
        line = line.strip()
        if not line:
            break

        g.add_edge(*line.split("|"))

    candidates = [l.strip() for l in lines]


middles = []
failed = []


def are_pages_ordered(nodes):
    path_nodes = set()

    try:
        for start, end in zip(nodes, nodes[1:]):
            path_nodes.update(nx.shortest_path(g, start, end))
    except nx.NetworkXNoPath:
        return False

    path = nx.subgraph(g, path_nodes)
    try:
        nx.find_cycle(path, orientation="original")
        return False
    except nx.NetworkXNoCycle:
        # middles.append(int(nodes[int((len(nodes) -1) / 2)]))
        # print(nodes, middles[-1])
        return True


failures = []


for can in candidates:
    nodes = can.split(",")
    if not are_pages_ordered(nodes):
        failures.append(nodes)


middles = []

for fail in failures:
    sub_g = nx.subgraph(g, fail)
    nodes = list(nx.topological_sort(sub_g))
    middles.append(int(nodes[int((len(nodes) - 1) / 2)]))

print(sum(middles))
