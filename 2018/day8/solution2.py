from uuid import uuid4

from toolz import memoize
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

    metadata_refs = {}

    for i in range(num_children):

        child_node, remainder = build_node(remainder)
        metadata_refs[i + 1] = child_node

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
        metadata=[metadata_refs[i] for i in metadata if i in metadata_refs],
        childless=sum(metadata)
    )

    return node_id, remainder[num_metadata:]


top_node, remainder = build_node(starting_numbers)
if remainder:
    raise ValueError("Didn't work")


@memoize
def total_nodes(node):

    if tree.node[node]['metadata']:

        return sum([
            total_nodes(n)
            for n in tree.node[node]['metadata']
        ])

    else:
        return tree.node[node]['childless']


print(total_nodes(top_node))


# import matplotlib.pyplot as plt
# pos = nx.nx_agraph.graphviz_layout(tree, prog='dot')
# nx.draw_networkx(tree, pos=pos)
# plt.show()
