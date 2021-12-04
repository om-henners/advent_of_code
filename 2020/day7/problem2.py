import re

import matplotlib.pyplot as plt
import networkx as nx
from sklearn.preprocessing import minmax_scale


bag_match = re.compile(r"(\d+) (.+?) bags?")
rules = nx.DiGraph()


for line in open('input'):
    container, contents = line.split(' bags contain ')

    for match in bag_match.finditer(contents):
        rules.add_edge(
            container,
            match.group(2),
            quantity=int(match.group(1))
        )


shiny_gold_container = nx.subgraph(rules, {'shiny gold'} | nx.descendants(rules, 'shiny gold'))

# work out where the endpoints are
end_points = {
    n for n in shiny_gold_container.nodes()
    if shiny_gold_container.out_degree(n) == 0  # it's already a subgraph of descendants
}

# turn the paths into a branching tree to get unique paths
branching_gold = nx.dag_to_branching(shiny_gold_container)
branching_gold_source = [  # the 'shiny gold' node, as many times as it appears (should be once
    n for n in branching_gold.nodes()
    if branching_gold.in_degree(n) == 0
]
assert len(branching_gold_source) == 1
branching_gold_source = branching_gold_source[0]

# now a depth first traversal of the edges
for source, dest in nx.dfs_edges(branching_gold, branching_gold_source):

    source_name = branching_gold.nodes[source]['source']
    dest_name = branching_gold.nodes[dest]['source']
    single_quantity = shiny_gold_container.edges[(source_name, dest_name)]['quantity']

    if source == branching_gold_source:
        num_bags = 1
    else:
        num_bags = sum([
            branching_gold.edges[(n, source)]['quantity']
            for n in branching_gold.predecessors(source)
        ])

    print(source_name, dest_name, single_quantity, '-->', num_bags * single_quantity)

    branching_gold.edges[(source, dest)]['quantity'] = num_bags * single_quantity


pos = nx.nx_pydot.graphviz_layout(branching_gold, prog='dot')
quantities = [quantity for (*_, quantity) in branching_gold.edges(data='quantity')]
colours = [
    'red' if source in end_points else 'blue'
    for _, source in branching_gold.nodes(data='source')
]
node_labels = dict(branching_gold.nodes(data='source'))
edge_labels = {
    tuple(edge): quantity
    for *edge, quantity in branching_gold.edges(data='quantity')
}
nx.draw_networkx(
    branching_gold,
    pos=pos,
    width=minmax_scale(quantities, (1, 10)),
    node_color=colours,
    labels=node_labels,
)
nx.draw_networkx_edge_labels(
    branching_gold,
    pos=pos,
    edge_labels=edge_labels
)

plt.show()

print(sum(quantities))
