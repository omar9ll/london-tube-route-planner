import csv
import math
from graph_algorithms import DirectedWeightedGraph


def load_station_data(stations_file):
    station_data = {}

    with open(stations_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            station_id = int(row["id"])
            station_data[station_id] = {
                "name": row["name"],
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "zone": float(row["zone"]),
                "total_lines": int(row["total_lines"])
            }

    return station_data



def add_connection(G, edge_lines, station1, station2, line, time):
    # If same station pair appears more than once, keep smallest travel time
    if not G.are_connected(station1, station2):
        G.add_edge(station1, station2, time)
    elif time < G.w(station1, station2):
        G.add_edge(station1, station2, time)

    # Keeps track of all lines connecting to this pair
    if (station1, station2) not in edge_lines:
        edge_lines[(station1, station2)] = set()
    edge_lines[(station1, station2)].add(line)


def build_london_graph(stations_file, connections_file):
    station_data = load_station_data(stations_file)
    G = DirectedWeightedGraph()
    edge_lines = {}

    for station_id in station_data:
        G.add_node(station_id)

    with open(connections_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            station1 = int(row["station1"])
            station2 = int(row["station2"])
            line = int(row["line"])
            time = int(row["time"])

            # Tube connection usable both ways
            add_connection(G, edge_lines, station1, station2, line, time)
            add_connection(G, edge_lines, station2, station1, line, time)

    return G, station_data, edge_lines


def haversine_distance(lat1, lon1, lat2, lon2):
    # get distance in kilometres.
    radius = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return radius * c


def compute_max_speed(station_data, connections_file):
    # convert straight line distance into optimistic time estimate (speed is km per minute)

    max_speed = 0.0

    with open(connections_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            station1 = int(row["station1"])
            station2 = int(row["station2"])
            time = int(row["time"])

            if time == 0:
                continue

            lat1 = station_data[station1]["latitude"]
            lon1 = station_data[station1]["longitude"]
            lat2 = station_data[station2]["latitude"]
            lon2 = station_data[station2]["longitude"]

            distance = haversine_distance(lat1, lon1, lat2, lon2)
            speed = distance / time

            if speed > max_speed:
                max_speed = speed

    if max_speed == 0:
        return 1.0

    return max_speed


def build_heuristic(station_data, destination, max_speed):
    # Returns dictionary h where h[node] estimates remaining travel time from that node to destination.
    heuristic = {}

    dest_lat = station_data[destination]["latitude"]
    dest_lon = station_data[destination]["longitude"]

    for station_id in station_data:
        lat = station_data[station_id]["latitude"]
        lon = station_data[station_id]["longitude"]

        straight_line_distance = haversine_distance(lat, lon, dest_lat, dest_lon)
        heuristic[station_id] = straight_line_distance / max_speed

    return heuristic