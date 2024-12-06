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

# nx.write_gexf(g, "advent.gexf")

print(nx.find_cycle(g, orientation="original"))

middles = []
failed = 0

for can in candidates:
    nodes = can.split(",")

    path_nodes = set()

    try:
        for start, end in zip(nodes, nodes[1:]):
            path_nodes.update(nx.shortest_path(g, start, end))
    except nx.NetworkXNoPath:
        failed += 1
        print("doh")
        continue

    path = nx.subgraph(g, path_nodes)
    try:
        nx.find_cycle(path, orientation="original")
        failed += 1
    except nx.NetworkXNoCycle:
        middles.append(int(nodes[int((len(nodes) - 1) / 2)]))
        # print(nodes, middles[-1])

print(sum(middles))
print(len(middles), failed, len(candidates))
