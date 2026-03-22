import networkx as nx
from collections import defaultdict

def wash_trading_signal(G: nx.DiGraph, target: str) -> float:
    cycles = 0
    total_edges = G.number_of_edges()
    if total_edges == 0:
        return 0.0

    for u, v in G.edges():
        if G.has_edge(v, u):
            cycles += 1

    return min(cycles / total_edges, 1.0)

def fan_out_signal(G: nx.DiGraph, target: str, window: int = 3600) -> float:
    if target not in G:
        return 0.0

    outgoing = [(v, G[target][v]["timestamps"]) for v in G.successors(target)]
    if not outgoing:
        return 0.0

    all_timestamps = []
    for _, timestamps in outgoing:
        all_timestamps.extend(timestamps)

    if len(all_timestamps) < 2:
        return 0.0

    all_timestamps.sort()
    max_burst = 0
    for i in range(len(all_timestamps)):
        window_txns = [t for t in all_timestamps if all_timestamps[i] <= t <= all_timestamps[i] + window]
        unique_receivers = set()
        for v, timestamps in outgoing:
            if any(all_timestamps[i] <= t <= all_timestamps[i] + window for t in timestamps):
                unique_receivers.add(v)
        max_burst = max(max_burst, len(unique_receivers))

    return min(max_burst / 20, 1.0)

def clustering_signal(G: nx.DiGraph, target: str) -> float:
    if G.number_of_nodes() < 3:
        return 0.0

    neighbors = set(G.successors(target)) | set(G.predecessors(target))
    if not neighbors:
        return 0.0

    total_volume = sum(G[u][v]["amount"] for u, v in G.edges())
    if total_volume == 0:
        return 0.0

    neighbor_volume = 0
    for u, v in G.edges():
        if u in neighbors or v in neighbors or u == target or v == target:
            neighbor_volume += G[u][v]["amount"]

    return min(neighbor_volume / total_volume, 1.0)

def velocity_signal(G: nx.DiGraph, target: str) -> float:
    if target not in G:
        return 0.0

    all_timestamps = []
    for v in G.successors(target):
        all_timestamps.extend(G[target][v]["timestamps"])
    for u in G.predecessors(target):
        all_timestamps.extend(G[u][target]["timestamps"])

    if len(all_timestamps) < 2:
        return 0.0

    all_timestamps.sort()
    intervals = [all_timestamps[i+1] - all_timestamps[i] for i in range(len(all_timestamps)-1)]
    avg_interval = sum(intervals) / len(intervals)

    if avg_interval < 60:
        return 1.0
    elif avg_interval < 300:
        return 0.7
    elif avg_interval < 3600:
        return 0.3
    else:
        return 0.0