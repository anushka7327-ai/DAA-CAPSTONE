"""Interactive demo on a small named city map."""
from graph import Graph
from algorithms import dijkstra, bellman_ford, reconstruct_path

ROADS = [
    ("Airport", "Cyber Hub", 12), ("Airport", "Sector 29", 18),
    ("Cyber Hub", "Sector 29", 6), ("Cyber Hub", "MG Road", 9),
    ("Sector 29", "Huda City Centre", 8), ("MG Road", "Huda City Centre", 5),
    ("MG Road", "Railway Station", 7), ("Huda City Centre", "Railway Station", 11),
    ("Railway Station", "Old Gurgaon", 4), ("Sector 29", "Old Gurgaon", 20),
]


def build_city():
    g = Graph()
    for u, v, w in ROADS:
        g.add_edge(u, v, w)
    return g


def main():
    g = build_city()
    places = sorted(g.vertices)
    print("Locations:", ", ".join(places))
    src = input("From: ").strip()
    dst = input("To:   ").strip()
    if src not in g.vertices or dst not in g.vertices:
        return print("Unknown location.")
    for name, algo in (("Dijkstra", dijkstra), ("Bellman-Ford", bellman_ford)):
        dist, prev = algo(g, src)
        path = reconstruct_path(prev, src, dst)
        print(f"\n[{name}] {' -> '.join(path)}  (cost: {dist[dst]} min)")


if __name__ == "__main__":
    main()
