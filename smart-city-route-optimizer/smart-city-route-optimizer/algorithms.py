"""Shortest-path algorithms: Dijkstra and Bellman-Ford."""
import heapq
import math


def dijkstra(graph, source):
    """O((V + E) log V) with a binary heap. Requires non-negative weights."""
    dist = {v: math.inf for v in graph.vertices}
    prev = {v: None for v in graph.vertices}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry
        for v, w in graph.adj[u]:
            if w < 0:
                raise ValueError("Dijkstra cannot handle negative weights")
            nd = d + w
            if nd < dist[v]:
                dist[v], prev[v] = nd, u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def bellman_ford(graph, source):
    """O(V * E). Handles negative weights; detects negative cycles."""
    dist = {v: math.inf for v in graph.vertices}
    prev = {v: None for v in graph.vertices}
    dist[source] = 0
    edges = list(graph.edges())
    for _ in range(len(graph.vertices) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v], prev[v] = dist[u] + w, u
                changed = True
        if not changed:  # early exit optimisation
            break
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("Negative cycle detected")
    return dist, prev


def reconstruct_path(prev, source, target):
    path, node = [], target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path if path and path[0] == source else []
