import re

import networkx as nx


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

print(nx.descendants(rules, 'shiny gold'))
print(len(nx.ancestors(rules, 'shiny gold')))
