import min_heap
import random

class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(G, source):
    pred = {} # Predecessor dictionary
    dist = {} # Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(source, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
    return dist


def bellman_ford(G, source):
    pred = {} # Predecessor dictionary
    dist = {} # Distance dictionary
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
    return dist

def dijkstra_approx(G, source, k):
    pred = {}
    dist = {}
    relax_count = {}

    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        relax_count[node] = 0

    Q.decrease_key(source, 0)
    dist[source] = 0

    while not Q.is_empty():
        current_element = Q.extract_min()
        u = current_element.value

        for v in G.adj[u]:
            if relax_count[v] < k:
                if dist[u] + G.w(u, v) < dist[v]:
                    dist[v] = dist[u] + G.w(u, v)
                    Q.decrease_key(v, dist[v])
                    pred[v] = u
                    relax_count[v] += 1

    return dist


def bellman_ford_approx(G, source, k):
    pred = {}
    dist = {}
    relax_count = {}

    nodes = list(G.adj.keys())

    for node in nodes:
        dist[node] = float("inf")
        relax_count[node] = 0

    dist[source] = 0

    for _ in range(G.number_of_nodes()):
        for u in nodes:
            for v in G.adj[u]:
                if relax_count[v] < k:
                    if dist[v] > dist[u] + G.w(u, v):
                        dist[v] = dist[u] + G.w(u, v)
                        pred[v] = u
                        relax_count[v] += 1

    return dist


def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total

def create_random_complete_graph(n,upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(1,upper))
    return G


#Assumes G represents its nodes as integers 0,1,...,(n-1)
def floyd_warshall(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

def init_d(G):
    n = G.number_of_nodes()
    d = [[float("inf") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d


def reconstruct_path(pred, s, d):
    if s == d:
        return [s]
    if d not in pred:
        return []
    path = [d]
    current = d
    while current != s:
        current = pred[current]
        path.append(current)
    path.reverse()
    return path


def a_star(G, s, d, h):
    """
    A* shortest path algorithm.

    Parameters:
        G : DirectedWeightedGraph
        s : source node
        d : destination node
        h : dictionary mapping node -> heuristic estimate to destination

    Returns:
        (pred, path)
        pred = predecessor dictionary
        path = shortest path from s to d as a list of nodes
    """

    pred = {}
    dist = {}
    closed = set()

    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    for node in nodes:
        dist[node] = float("inf")
        Q.insert(min_heap.Element(node, float("inf")))

    dist[s] = 0
    Q.decrease_key(s, h[s])

    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value

        if current_element.key == float("inf"):
            break
        
        if current_node in closed:
            continue

        closed.add(current_node)

        if current_node == d:
            return pred, reconstruct_path(pred, s, d)

        for neighbour in G.adj[current_node]:
            if neighbour in closed:
                continue

            tentative_g = dist[current_node] + G.w(current_node, neighbour)

            if tentative_g < dist[neighbour]:
                dist[neighbour] = tentative_g
                pred[neighbour] = current_node
                f_value = tentative_g + h[neighbour]
                Q.decrease_key(neighbour, f_value)

    return pred, []

