from graph_algorithms import DirectedWeightedGraph, a_star, dijkstra


def small_graph_test_1():
    G = DirectedWeightedGraph()
    for i in range(5):
        G.add_node(i)

    G.add_edge(0, 1, 2)
    G.add_edge(0, 2, 5)
    G.add_edge(1, 2, 1)
    G.add_edge(1, 3, 2)
    G.add_edge(2, 3, 1)
    G.add_edge(3, 4, 3)

    # admissible heuristic to destination 4
    h = {
        0: 4,
        1: 3,
        2: 2,
        3: 1,
        4: 0
    }

    pred, path = a_star(G, 0, 4, h)
    print("Test 1 path:", path)
    print("Test 1 pred:", pred)
    print("Dijkstra distances:", dijkstra(G, 0))


def zero_heuristic_test():
    G = DirectedWeightedGraph()
    for i in range(5):
        G.add_node(i)

    G.add_edge(0, 1, 2)
    G.add_edge(0, 2, 5)
    G.add_edge(1, 2, 1)
    G.add_edge(1, 3, 2)
    G.add_edge(2, 3, 1)
    G.add_edge(3, 4, 3)

    h = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

    pred, path = a_star(G, 0, 4, h)
    print("Zero heuristic path:", path)
    print("Zero heuristic pred:", pred)
    print("Dijkstra distances:", dijkstra(G, 0))


def no_path_test():
    G = DirectedWeightedGraph()
    for i in range(4):
        G.add_node(i)

    G.add_edge(0, 1, 2)
    G.add_edge(1, 2, 2)
    # node 3 unreachable

    h = {0: 1, 1: 1, 2: 1, 3: 0}

    pred, path = a_star(G, 0, 3, h)
    print("No path test path:", path)
    print("No path test pred:", pred)


if __name__ == "__main__":
    small_graph_test_1()
    print()
    zero_heuristic_test()
    print()
    no_path_test()