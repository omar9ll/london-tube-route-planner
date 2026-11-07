# 🚇 London Tube Route Planner — Shortest-Path Algorithms

Python implementation and benchmark of shortest-path algorithms (**Dijkstra, Bellman-Ford, A\*** and **Floyd-Warshall**) on a weighted, directed graph, applied to the real **London Underground** network (300+ stations, travel times between stations).

The project compares how much faster **A\*** finds routes than Dijkstra by using a geographic heuristic, and wraps everything in a clean object-oriented design.

## ✨ Highlights
- **Graph + algorithms from scratch**: custom directed weighted graph, indexed **min-heap priority queue** with `decrease_key`, Dijkstra, Bellman-Ford, A\* and Floyd-Warshall (all-pairs)
- **Approximation experiments**: limited-relaxation (k-bounded) Dijkstra and Bellman-Ford variants, measuring accuracy vs. k and graph size
- **London Underground graph**: built from station coordinates and connection travel times; keeps the fastest edge when multiple lines connect two stations
- **A\* heuristic**: straight-line (haversine) distance to the destination divided by the network's maximum observed speed, giving an **admissible** travel-time estimate
- **Benchmark over every station pair**: runtime and nodes explored for Dijkstra vs A\*, grouped by route type (same line, one transfer, several transfers) and trip length, with charts and CSV output
- **OOP refactor**: `Graph → WeightedGraph → HeuristicGraph` hierarchy and a **Strategy pattern** (`SPAlgorithm` with Dijkstra / Bellman-Ford / A\* implementations) behind a `ShortPathFinder`

## 📁 Files
| File | What it does |
|---|---|
| `graph_algorithms.py` | Graph class, Dijkstra, Bellman-Ford, k-approximations, Floyd-Warshall, A\*, path reconstruction |
| `min_heap.py` | Indexed min-heap priority queue with `decrease_key` |
| `london_graph.py` | Loads the Tube data, builds the graph, haversine heuristic |
| `london_experiments.py` | Dijkstra vs A\* benchmark across all station pairs (plots + CSV) |
| `shortest_path_finder.py` | OOP design: graph hierarchy + Strategy pattern for algorithms |
| `approximation_experiments.py` | Accuracy/runtime of k-bounded Dijkstra & Bellman-Ford |
| `floyd_warshall_experiments.py` | Correctness tests (incl. negative edges) and O(n³) runtime analysis |
| `astar_tests.py` | Small test cases for A\* (admissible / zero heuristic / unreachable target) |

## ▶️ Run it
```bash
pip install -r requirements.txt
python astar_tests.py              # quick correctness checks
python london_experiments.py       # full London benchmark (takes a while)
```

Use the planner from Python:
```python
from shortest_path_finder import build_london_heuristic_graph, ShortPathFinder, A_Star, Dijkstra

graph, stations = build_london_heuristic_graph("london_stations.csv", "london_connections.csv")
finder = ShortPathFinder()
finder.set_graph(graph)
finder.set_algorithm(A_Star())
print(finder.calc_short_path(1, 234))   # travel time between two station IDs
```

## 🛠️ Tech
Python · Matplotlib · Algorithms & data structures (graphs, heaps, shortest paths) · OOP design patterns

## 📄 Data
London Underground station and connection data from the open [nicola/tubemaps](https://github.com/nicola/tubemaps) dataset.

---
Originally built as a final project for an algorithms & software design course at McMaster University.
