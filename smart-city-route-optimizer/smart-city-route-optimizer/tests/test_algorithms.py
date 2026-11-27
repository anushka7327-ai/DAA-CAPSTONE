import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from graph import Graph, random_city
from algorithms import dijkstra, bellman_ford, reconstruct_path


def test_small_graph():
    g = Graph()
    for u, v, w in [("A", "B", 4), ("A", "C", 1), ("C", "B", 2), ("B", "D", 5)]:
        g.add_edge(u, v, w)
    dist, prev = dijkstra(g, "A")
    assert dist["B"] == 3 and dist["D"] == 8
    assert reconstruct_path(prev, "A", "D") == ["A", "C", "B", "D"]


@pytest.mark.parametrize("seed", range(5))
def test_both_algorithms_agree(seed):
    g = random_city(150, seed=seed)
    assert dijkstra(g, 0)[0] == bellman_ford(g, 0)[0]


def test_negative_edge_bellman_ford():
    g = Graph(directed=True)
    g.add_edge("A", "B", 4); g.add_edge("A", "C", 5); g.add_edge("C", "B", -3)
    assert bellman_ford(g, "A")[0]["B"] == 2


def test_negative_cycle_detected():
    g = Graph(directed=True)
    g.add_edge("A", "B", 1); g.add_edge("B", "C", -3); g.add_edge("C", "A", 1)
    with pytest.raises(ValueError):
        bellman_ford(g, "A")
