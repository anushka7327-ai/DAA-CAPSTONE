"""Compare Dijkstra vs Bellman-Ford across graph sizes."""
import csv
import time
from algorithms import dijkstra, bellman_ford
from graph import random_city

SIZES = [100, 250, 500, 1000, 2000]


def timeit(fn, g, src, repeats=3):
    best = float("inf")
    for _ in range(repeats):
        t = time.perf_counter()
        fn(g, src)
        best = min(best, time.perf_counter() - t)
    return best * 1000  # ms


def run():
    rows = []
    print(f"{'V':>6} {'E':>7} {'Dijkstra(ms)':>14} {'BellmanFord(ms)':>16} {'Ratio':>7}")
    for n in SIZES:
        g = random_city(n, seed=42)
        src = 0
        d, b = timeit(dijkstra, g, src), timeit(bellman_ford, g, src)
        rows.append((n, g.edge_count(), round(d, 3), round(b, 3)))
        print(f"{n:>6} {g.edge_count():>7} {d:>14.3f} {b:>16.3f} {b / d:>7.1f}x")
    with open("benchmark_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["vertices", "edges", "dijkstra_ms", "bellman_ford_ms"])
        w.writerows(rows)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.plot([r[0] for r in rows], [r[2] for r in rows], "o-", label="Dijkstra")
        plt.plot([r[0] for r in rows], [r[3] for r in rows], "s-", label="Bellman-Ford")
        plt.xlabel("Number of locations (V)"); plt.ylabel("Time (ms)")
        plt.title("Dijkstra vs Bellman-Ford"); plt.legend(); plt.grid(alpha=.3)
        plt.savefig("benchmark.png", dpi=150, bbox_inches="tight")
        print("Saved benchmark.csv and benchmark.png")
    except ImportError:
        print("matplotlib not installed - CSV saved only")


if __name__ == "__main__":
    run()
