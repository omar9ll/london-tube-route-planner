import csv
import time
import matplotlib.pyplot as plt
import min_heap
from graph_algorithms import reconstruct_path
from london_graph import build_london_graph, compute_max_speed, build_heuristic

# These versions of Dijkstra and A* are used for the London benchmark.
# They stop as soon as the destination is reached and count how many nodes are popped from the heap.


def dijkstra_to_dest(G, source, destination):
    pred = {}
    dist = {}
    closed = set()
    pq = min_heap.MinHeap([])

    for node in G.adj:
        dist[node] = float("inf")
        pq.insert(min_heap.Element(node, float("inf")))

    dist[source] = 0
    pq.decrease_key(source, 0)

    nodes_popped = 0

    while not pq.is_empty():
        current = pq.extract_min().value

        if current in closed:
            continue


        closed.add(current)
        nodes_popped += 1
        if current == destination:
            path = reconstruct_path(pred, source, destination)
            return pred, path, dist[current], nodes_popped

        for neighbour in G.adj[current]:
            if neighbour in closed:
                continue

            new_dist = dist[current] + G.w(current, neighbour)
            if new_dist < dist[neighbour]:
                dist[neighbour] = new_dist
                pred[neighbour] = current
                pq.decrease_key(neighbour, new_dist)

    return pred, [], float("inf"), nodes_popped


def a_star_to_dest(G, source, destination, h):
    pred = {}
    dist = {}
    closed = set()
    pq = min_heap.MinHeap([])

    for node in G.adj:
        dist[node] = float("inf")
        pq.insert(min_heap.Element(node, float("inf")))

    dist[source] = 0
    pq.decrease_key(source, h[source])
    nodes_popped = 0

    while not pq.is_empty():
        current = pq.extract_min().value

        if current in closed:
            continue
        closed.add(current)
        nodes_popped += 1

        if current == destination:
            path = reconstruct_path(pred, source, destination)
            return pred, path, dist[current], nodes_popped

        for neighbour in G.adj[current]:
            if neighbour in closed:
                continue

            new_dist = dist[current] + G.w(current, neighbour)

            if new_dist < dist[neighbour]:
                dist[neighbour] = new_dist
                pred[neighbour] = current
                pq.decrease_key(neighbour, new_dist + h[neighbour])


    return pred, [], float("inf"), nodes_popped


def classify_route_category(path, edge_lines):
    # Tries to stay on the same line as long as possible.
    # Then the route is grouped into same line, adjacent lines, or several transfers.

    if len(path) <= 1:
        return "same line"

    current_lines = set(edge_lines[(path[0], path[1])])
    lines_used = 1

    for i in range(1, len(path) - 1):
        next_lines = set(edge_lines[(path[i], path[i + 1])])
        overlap = current_lines.intersection(next_lines)
        if len(overlap) > 0:
            current_lines = overlap
        else:
            lines_used += 1
            current_lines = next_lines

    if lines_used == 1:
        return "same line"
    if lines_used == 2:
        return "adjacent lines"
    return "several transfers"


def save_results_csv(results, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "source",
            "destination",
            "source_name",
            "destination_name",
            "travel_time",
            "dijkstra_runtime_ms",
            "astar_runtime_ms",
            "dijkstra_nodes_popped",
            "astar_nodes_popped",
            "path_length",
            "line_category"
        ])

        for row in results:
            writer.writerow([
                row["source"],
                row["destination"],
                row["source_name"],
                row["destination_name"],
                row["travel_time"],
                row["dijkstra_runtime_ms"],
                row["astar_runtime_ms"],
                row["dijkstra_nodes_popped"],
                row["astar_nodes_popped"],
                row["path_length"],
                row["line_category"]
            ])


def average(values):
    if len(values) == 0:
        return 0
    return sum(values) / len(values)


def plot_runtime_by_category(results):
    categories = ["same line", "adjacent lines", "several transfers"]
    dijkstra_means = []
    astar_means = []

    for category in categories:
        rows = [row for row in results if row["line_category"] == category]
        dijkstra_means.append(average([row["dijkstra_runtime_ms"] for row in rows]))
        astar_means.append(average([row["astar_runtime_ms"] for row in rows]))

    x = [0, 1, 2]
    width = 0.35


    plt.figure(figsize=(9, 5))
    plt.bar([i - width / 2 for i in x], dijkstra_means, width=width, label="Dijkstra")
    plt.bar([i + width / 2 for i in x], astar_means, width=width, label="A*")
    plt.xticks(x, categories)
    plt.ylabel("Average runtime (ms)")
    plt.title("Average runtime by station-pair category")
    plt.legend()
    plt.tight_layout()
    plt.savefig("london_runtime_by_category.png", dpi=200)
    plt.close()


def plot_nodes_by_category(results):
    categories = ["same line", "adjacent lines", "several transfers"]
    dijkstra_means = []
    astar_means = []

    for category in categories:
        rows = [row for row in results if row["line_category"] == category]
        dijkstra_means.append(average([row["dijkstra_nodes_popped"] for row in rows]))
        astar_means.append(average([row["astar_nodes_popped"] for row in rows]))

    x = [0, 1, 2]
    width = 0.35

    plt.figure(figsize=(9, 5))
    plt.bar([i - width / 2 for i in x], dijkstra_means, width=width, label="Dijkstra")
    plt.bar([i + width / 2 for i in x], astar_means, width=width, label="A*")
    plt.xticks(x, categories)
    plt.ylabel("Average nodes popped")

    plt.title("Average nodes explored by station-pair category")
    plt.legend()
    plt.tight_layout()
    plt.savefig("london_nodes_by_category.png", dpi=200)
    plt.close()


def make_travel_time_buckets(results, bucket_size):
    buckets = {}

    for row in results:
        start = (row["travel_time"] // bucket_size) * bucket_size
        end = start + bucket_size - 1
        label = str(start) + "-" + str(end)

        if label not in buckets:
            buckets[label] = []

        buckets[label].append(row)

    ordered_labels = sorted(
        buckets.keys(),
        key=lambda label: int(label.split("-")[0])
    )

    return ordered_labels, buckets


def plot_runtime_by_travel_time_bucket(results, bucket_size=5):
    labels, buckets = make_travel_time_buckets(results, bucket_size)

    dijkstra_means = []
    astar_means = []

    for label in labels:
        rows = buckets[label]
        dijkstra_means.append(average([row["dijkstra_runtime_ms"] for row in rows]))
        astar_means.append(average([row["astar_runtime_ms"] for row in rows]))

    plt.figure(figsize=(10, 5))
    plt.plot(labels, dijkstra_means, marker="o", label="Dijkstra")
    plt.plot(labels, astar_means, marker="o", label="A*")
    plt.xlabel("Shortest-path travel time bucket")
    plt.ylabel("Average runtime (ms)")
    plt.title("Average runtime by shortest-path travel time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("london_runtime_by_travel_time.png", dpi=200)
    plt.close()


def print_summary(results):
    print("\nOverall Summary")
    print("Number of station pairs tested:", len(results))
    print("Average Dijkstra runtime (ms):", average([row["dijkstra_runtime_ms"] for row in results]))
    print("Average A* runtime (ms):", average([row["astar_runtime_ms"] for row in results]))
    print("Average Dijkstra nodes popped:", average([row["dijkstra_nodes_popped"] for row in results]))
    print("Average A* nodes popped:", average([row["astar_nodes_popped"] for row in results]))

    categories = ["same line", "adjacent lines", "several transfers"]

    for category in categories:
        rows = [row for row in results if row["line_category"] == category]
        print("\nCategory:", category)
        print("Pairs:", len(rows))
        print("Average travel time:", average([row["travel_time"] for row in rows]))
        print("Average Dijkstra runtime (ms):", average([row["dijkstra_runtime_ms"] for row in rows]))
        print("Average A* runtime (ms):", average([row["astar_runtime_ms"] for row in rows]))
        print("Average Dijkstra nodes popped:", average([row["dijkstra_nodes_popped"] for row in rows]))
        print("Average A* nodes popped:", average([row["astar_nodes_popped"] for row in rows]))


def print_best_and_worst_examples(results):
    ordered = sorted(
        results,
        key=lambda row: row["dijkstra_nodes_popped"] - row["astar_nodes_popped"],
        reverse=True
    )

    print("\nExamples Where A* Helped The Most")
    for row in ordered[:5]:
        print(
            row["source_name"], "->", row["destination_name"],
            "| category =", row["line_category"],
            "| travel time =", row["travel_time"],
            "| Dijkstra nodes =", row["dijkstra_nodes_popped"],
            "| A* nodes =", row["astar_nodes_popped"]
        )

    print("\nExampels Where There Were Most Similar")
    ordered_small = sorted(
        results,
        key=lambda row: abs(row["dijkstra_nodes_popped"] - row["astar_nodes_popped"])
    )

    for row in ordered_small[:5]:
        print(
            row["source_name"], "->", row["destination_name"],
            "| category =", row["line_category"],
            "| travel time =", row["travel_time"],
            "| Dijkstra nodes =", row["dijkstra_nodes_popped"],
            "| A* nodes =", row["astar_nodes_popped"]
        )


def run_experiment_suite():
    G, station_data, edge_lines = build_london_graph(
        "london_stations.csv",
        "london_connections.csv"
    )

    max_speed = compute_max_speed(station_data, "london_connections.csv")

    heuristics = {}
    for destination in station_data:
        heuristics[destination] = build_heuristic(station_data, destination, max_speed)

    station_ids = list(G.adj.keys())
    results = []

    pair_count = 0
    total_pairs = len(station_ids) * (len(station_ids) - 1)

    for source in station_ids:
        for destination in station_ids:
            if source == destination:
                continue

            pair_count += 1
            if pair_count % 10000 == 0:
                print("Processed", pair_count, "out of", total_pairs, "pairs")

            start_time = time.perf_counter()
            _, dijkstra_path, dijkstra_dist, dijkstra_nodes = dijkstra_to_dest(G, source, destination)
            end_time = time.perf_counter()
            dijkstra_runtime_ms = (end_time - start_time) * 1000

            start_time = time.perf_counter()
            _, _, astar_dist, astar_nodes = a_star_to_dest(
                G,
                source,
                destination,
                heuristics[destination]
            )
            end_time = time.perf_counter()
            astar_runtime_ms = (end_time - start_time) * 1000

            if dijkstra_dist != astar_dist:
                print("Distance mismatch found between", source, "and", destination)
                print("Dijkstra distance:", dijkstra_dist)
                print("A* distance:", astar_dist)
                return

            if dijkstra_dist == float("inf"):
                continue

            line_category = classify_route_category(dijkstra_path, edge_lines)

            results.append({
                "source": source,
                "destination": destination,
                "source_name": station_data[source]["name"],
                "destination_name": station_data[destination]["name"],
                "travel_time": dijkstra_dist,
                "dijkstra_runtime_ms": dijkstra_runtime_ms,
                "astar_runtime_ms": astar_runtime_ms,
                "dijkstra_nodes_popped": dijkstra_nodes,
                "astar_nodes_popped": astar_nodes,
                "path_length": len(dijkstra_path),
                "line_category": line_category
            })

    save_results_csv(results, "london_results.csv")
    plot_runtime_by_category(results)
    plot_nodes_by_category(results)
    plot_runtime_by_travel_time_bucket(results, bucket_size=5)
    print_summary(results)
    print_best_and_worst_examples(results)


if __name__ == "__main__":
    run_experiment_suite()