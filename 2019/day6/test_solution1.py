#!/usr/bin/env python
"""Tests for solution 1 for day 6.

Graph theory for the win!
"""
import pytest
import networkx as nx

import solution1


TEST_ORBITS = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""


def test_create_directed_graph():
    """
    Test the creation methods to read in the data and store as an edgelist.
    """
    graph = solution1.create_directed_graph(TEST_ORBITS)

    assert isinstance(graph, nx.DiGraph)

    num_nodes = set()
    for line in TEST_ORBITS.split():
        num_nodes.update(line.split(')'))

    assert len(graph) == len(num_nodes)


def test_count_orbits():
    """
    Test counting the "orbits" (reaally, descendents of all nodes)
    """
    graph = solution1.create_directed_graph(TEST_ORBITS)

    assert solution1.count_orbits(graph) == 42
