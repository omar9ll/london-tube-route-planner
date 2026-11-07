import matplotlib.pyplot as plt
import time
from graph_algorithms import *

def experiment1():
    n = 75
    upper = 50
    k_values = [1, 2, 3, 5, 10, 20]

    G = create_random_complete_graph(n, upper)

    true_dist = dijkstra(G, 0)
    true_total = total_dist(true_dist)

    dijkstra_results = []
    bellman_results = []

    for k in k_values:
        d_app = dijkstra_approx(G, 0, k)
        b_app = bellman_ford_approx(G, 0, k)

        dijkstra_results.append(total_dist(d_app))
        bellman_results.append(total_dist(b_app))

    plt.figure()
    plt.plot(k_values, dijkstra_results, label="Dijkstra Approx")
    plt.plot(k_values, bellman_results, label="Bellman-Ford Approx")
    plt.axhline(true_total, linestyle="--", label="True Dijkstra")
    plt.xlabel("k (max relaxations)")
    plt.ylabel("Total Distance")
    plt.title("Experiment 1: Effect of k")
    plt.legend()
    plt.savefig("exp1_k_effect.png")
    plt.show()

def experiment2():
    upper = 50
    k = 2
    n_values = [20, 40, 60, 80, 100]

    dijkstra_results = []
    bellman_results = []

    for n in n_values:
        G = create_random_complete_graph(n, upper)

        d_app = dijkstra_approx(G, 0, k)
        b_app = bellman_ford_approx(G, 0, k)

        dijkstra_results.append(total_dist(d_app))
        bellman_results.append(total_dist(b_app))

    plt.figure()
    plt.plot(n_values, dijkstra_results, label="Dijkstra Approx")
    plt.plot(n_values, bellman_results, label="Bellman-Ford Approx")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Total Distance")
    plt.title("Experiment 2: Effect of Graph Size")
    plt.legend()
    plt.savefig("exp2_graph_size.png")
    plt.show()


def experiment3():
    n = 100
    upper = 50
    k_values = [1, 2, 3, 5, 10, 20]

    G = create_random_complete_graph(n, upper)
    times = []

    for k in k_values:
        start = time.time()
        dijkstra_approx(G, 0, k)
        end = time.time()
        times.append(end - start)

    plt.figure()
    plt.plot(k_values, times)
    plt.xlabel("k")
    plt.ylabel("Runtime (seconds)")
    plt.title("Experiment 3: Runtime vs k")
    plt.savefig("exp3_runtime.png")
    plt.show()

if __name__ == "__main__":
    experiment1()
    experiment2()
    experiment3()