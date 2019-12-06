#!/usr/bin/env python
"""Day 6 solution 1

Before you use your map data to plot a course, you need to make sure
it wasn't corrupted during the download. To verify maps, the Universal
Orbit Map facility uses orbit count checksums - the total number of
direct orbits (like the one shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This
chain can be any number of objects long: if A orbits B, B orbits C,
and C orbits D, then A indirectly orbits D.
"""
import networkx as nx


def create_directed_graph(orbits: str) -> nx.DiGraph:
    """
    Turn the data into a directed graph.
    """
    orbits = orbits.split()

    graph = nx.parse_edgelist(
        orbits,
        delimiter=')',
        create_using=nx.DiGraph
    )

    return graph


def count_orbits(dg: nx.DiGraph) -> int:
    """
    Count  orbits (ie total number of descendaants of each node)
    """
    # dependding on the  direction of each graph you could use either
    # descendants or ancestors

    total = 0

    for node in dg:
        total += len(nx.descendants(dg, node))

    return total


def main():
    """Main runner for puzzle"""
    with open('input') as f:
        graph = create_directed_graph(f.read())
        print(count_orbits(graph))


if __name__ == '__main__':
    main()
