from uuid import uuid4

import networkx as nx


ROUTES = nx.Graph()
DIRECTION = {
    'N': (0, 1),
    'E': (1, 0),
    'W': (-1, 0),
    'S': (0, -1)
}

def parse_tree(text, current_node):

    start_node = current_node
    i = 0
    while i < len(text):

        try:
            change = DIRECTION[text[i]]
            new_location = current_node[0] + change[0], current_node[1] + change[1]
            ROUTES.add_edge(current_node, new_location)
            current_node = new_location
        except KeyError:
            if text[i] == '(':
                current_node, step =  parse_tree(text[i + 1:], current_node)
                i += step + 1

            elif text[i] == ')':
                return current_node, i

            elif text[i] == '|':
                current_node = start_node

            elif text[i] == '$':
                return current_node, i

        i += 1

    return current_node, i


# expr = '''^WNE$'''
# expr = '''^ENWWW(NEEE|SSE(EE|N))$'''
# expr = '''^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'''
# expr = '''^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'''
expr = open('input.txt').read().strip()

start_node = (0, 0)
ROUTES.add_node(start_node)
end_node, _ = parse_tree(expr[1:], start_node)

import matplotlib.pyplot as plt

nx.draw_networkx(ROUTES, pos={n: n for n in ROUTES.nodes()})
plt.show()

shortest_paths = nx.shortest_path_length(ROUTES, start_node)
print('solution 1:', max(shortest_paths.values()))

print(len(list(filter(lambda k: shortest_paths[k] >= 1000, shortest_paths))))