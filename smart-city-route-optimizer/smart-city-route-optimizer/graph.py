"""Graph representation: locations = vertices, roads = weighted edges."""
import random
from collections import defaultdict


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = defaultdict(list)  # u -> [(v, weight)]
        self.vertices = set()

    def add_edge(self, u, v, w):
        self.vertices.update((u, v))
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))

    def edges(self):
        """Yield every directed edge (u, v, w)."""
        for u in self.adj:
            for v, w in self.adj[u]:
                yield u, v, w

    def __len__(self):
        return len(self.vertices)

    def edge_count(self):
        return sum(len(n) for n in self.adj.values())


def random_city(n, extra_edges_factor=3, max_w=50, seed=None):
    """Connected random road network: a spanning chain plus random extra roads."""
    rng = random.Random(seed)
    g = Graph()
    nodes = list(range(n))
    rng.shuffle(nodes)
    for i in range(1, n):  # guarantees connectivity
        g.add_edge(nodes[i - 1], nodes[i], rng.randint(1, max_w))
    for _ in range(n * extra_edges_factor):
        u, v = rng.sample(range(n), 2)
        g.add_edge(u, v, rng.randint(1, max_w))
    return g
