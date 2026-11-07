import math
import random
import time
import matplotlib.pyplot as plt
from graph_algorithms import DirectedWeightedGraph, floyd_warshall


def make_dense_graph(n, max_weight=20, allow_negative=False):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(n):
            if i != j:
                if allow_negative:
                    w = random.randint(-5, max_weight)
                else:
                    w = random.randint(1, max_weight)
                G.add_edge(i, j, w)

    return G


def small_manual_test_positive():
    G = DirectedWeightedGraph()
    for i in range(4):
        G.add_node(i)

    G.add_edge(0, 1, 3)
    G.add_edge(0, 2, 10)
    G.add_edge(1, 2, 2)
    G.add_edge(2, 3, 1)
    G.add_edge(1, 3, 8)

    D = floyd_warshall(G)
    print("Positive-weight graph result:")
    for row in D:
        print(row)


def small_manual_test_negative_no_cycle():
    G = DirectedWeightedGraph()
    for i in range(4):
        G.add_node(i)

    G.add_edge(0, 1, 4)
    G.add_edge(0, 2, 5)
    G.add_edge(1, 2, -2)
    G.add_edge(2, 3, 3)
    G.add_edge(1, 3, 6)

    D = floyd_warshall(G)
    print("Negative-weight graph (no negative cycle) result:")
    for row in D:
        print(row)


def small_manual_test_negative_cycle():
    G = DirectedWeightedGraph()
    for i in range(3):
        G.add_node(i)

    G.add_edge(0, 1, 1)
    G.add_edge(1, 2, -3)
    G.add_edge(2, 0, 1)

    D = floyd_warshall(G)
    print("Negative-cycle graph result:")
    for row in D:
        print(row)


def runtime_experiment():
    sizes = [10, 20, 30, 40, 50, 60, 70, 80]
    times = []

    for n in sizes:
        G = make_dense_graph(n, max_weight=20, allow_negative=False)
        start = time.perf_counter()
        floyd_warshall(G)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        print(f"n={n}, time={elapsed:.6f}s")

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times, marker='o')
    plt.xlabel("Number of nodes n")
    plt.ylabel("Runtime (seconds)")
    plt.title("Floyd-Warshall Runtime vs Number of Nodes")
    plt.grid(True)
    plt.savefig("floyd_warshall_runtime.png")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot([math.log(x) for x in sizes], [math.log(y) for y in times], marker='o')
    plt.xlabel("log(n)")
    plt.ylabel("log(runtime)")
    plt.title("Floyd-Warshall Log-Log Runtime Plot")
    plt.grid(True)
    plt.savefig("floyd_warshall_runtime_loglog.png")
    plt.show()


if __name__ == "__main__":
    small_manual_test_positive()
    print()
    small_manual_test_negative_no_cycle()
    print()
    small_manual_test_negative_cycle()
    print()
    runtime_experiment()