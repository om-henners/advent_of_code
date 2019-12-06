#!/usr/bin/env python
"""Solution to part 2


You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you move from any object to an object orbiting or orbited by that object.
"""
import networkx as nx

import solution1


def main():
    """
    Get the graph, make it undirected and find the route between YOU and SAN.

    Having found the route subtract 2 (since we care about where YOU and SAN are orbeting) and print the result.
    """
    with open('input') as f:
        graph = solution1.create_directed_graph(f.read()).to_undirected()
        print(nx.shortest_path_length(graph, 'YOU', 'SAN') - 2)


if __name__ == '__main__':
    main()
