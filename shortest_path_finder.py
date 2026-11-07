from abc import ABC, abstractmethod
import csv
from graph_algorithms import dijkstra, bellman_ford, a_star
from london_graph import load_station_data, compute_max_speed, build_heuristic

class Graph(ABC):
    def __init__(self):
        self.adj = {}

    def get_adj_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    
    @abstractmethod
    def add_edge(self, start, end, weight):
        if start not in self.adj:
            self.add_node(start)
        if end not in self.adj:
            self.add_node(end)

        if end not in self.adj[start]:
            self.adj[start].append(end)

    def get_num_of_nodes(self):
        return len(self.adj)


    def number_of_nodes(self):
        return self.get_num_of_nodes()


class WeightedGraph(Graph):

    def __init__(self):
        super().__init__()
        self.weights = {}

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def add_edge(self, start, end, weight):
        super().add_edge(start, end, weight)
        self.weights[(start, end)] = weight

    def w(self, node1, node2):
        return self.weights[(node1, node2)]


class HeuristicGraph(WeightedGraph):

    def __init__(self):
        super().__init__()
        self.station_data = {}
        self.max_speed = 0

    
    def set_station_data(self, station_data):
        self.station_data = station_data

    def get_station_data(self):
        return self.station_data

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def get_max_speed(self):
        return self.max_speed


class SPAlgorithm(ABC):

    @abstractmethod
    def calc_sp(self, graph, source, dest):
        pass


class Dijkstra(SPAlgorithm):

    def calc_sp(self, graph, source, dest):
        dist = dijkstra(graph, source)
        return dist[dest]


class Bellman_Ford(SPAlgorithm):
    def calc_sp(self, graph, source, dest):
        dist = bellman_ford(graph, source)
        return dist[dest]


class A_Star(SPAlgorithm):
    def calc_sp(self, graph, source, dest):
        heuristic = build_heuristic(
            graph.get_station_data(),
            dest,
            graph.get_max_speed()
        )
        _, path = a_star(graph, source, dest, heuristic)

        if len(path) == 0:
            return float("inf")

        total = 0

        for i in range(len(path) - 1):
            total += graph.w(path[i], path[i + 1])

        return total


class ShortPathFinder:

    def __init__(self):
        self.graph = None
        self.algorithm = None

    def set_graph(self, graph):
        self.graph = graph

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def calc_short_path(self, source, dest):
        if self.graph is None:
            raise ValueError("Graph has not been set.")
        
        if self.algorithm is None:
            raise ValueError("Algorithm has not been set.")

        return self.algorithm.calc_sp(self.graph, source, dest)


def add_london_connection(graph, station1, station2, time):
    if not graph.are_connected(station1, station2):
        graph.add_edge(station1, station2, time)

    elif time < graph.w(station1, station2):
        graph.add_edge(station1, station2, time)


def build_london_heuristic_graph(stations_file, connections_file, destination=None):
    station_data = load_station_data(stations_file)
    graph = HeuristicGraph()

    for station_id in station_data:
        graph.add_node(station_id)
    with open(connections_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            station1 = int(row["station1"])
            station2 = int(row["station2"])
            time = int(row["time"])

            add_london_connection(graph, station1, station2, time)
            add_london_connection(graph, station2, station1, time)

    max_speed = compute_max_speed(station_data, connections_file)
    graph.set_station_data(station_data)
    graph.set_max_speed(max_speed)

    return graph, station_data