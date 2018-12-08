from itertools import chain
from uuid import uuid4

import networkx as nx


data = open('input.txt').read().strip()
# data = open('sample_input.txt').read().strip()
starting_numbers = [int(i) for i in data.split()]
tree = nx.DiGraph()


def build_node(numbers):
    node_id = uuid4()

    num_children = numbers[0]
    num_metadata = numbers[1]

    remainder = numbers[2:]

    for i in range(num_children):

        child_node, remainder = build_node(remainder)

        tree.add_edge(
            node_id,
            child_node
        )

    metadata = remainder[:num_metadata]
    if len(metadata) < num_metadata:
        raise ValueError("Missing metadata")

    tree.add_node(
        node_id,
        details=(num_children, num_metadata),
        metadata=metadata
    )

    return node_id, remainder[num_metadata:]


top_node, remainder = build_node(starting_numbers)
if remainder:
    raise ValueError("Didn't work")

print(sum(chain.from_iterable(
    pair[1] for pair in
    tree.nodes(data='metadata')
    )))

import matplotlib.pyplot as plt
pos = nx.nx_agraph.graphviz_layout(tree, prog='dot')
nx.draw_networkx(tree, pos=pos, with_labels=False)
plt.show()
