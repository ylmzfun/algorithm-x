"""
Shortest path algorithms.

Contains:
- Dijkstra (O(E log V) with min-heap, path reconstruction)
- Bellman-Ford (negative edges, negative cycle detection)
- Floyd-Warshall (all-pairs shortest paths)
- SPFA (Shortest Path Faster Algorithm)
"""

import heapq
from typing import List, Optional, Tuple


INF = float("inf")


# ======================================================================
# Dijkstra
# ======================================================================

def dijkstra(
    n: int, edges: List[Tuple[int, int, int]], start: int
) -> Tuple[List[float], List[int]]:
    """
    Single-source shortest paths for non-negative edge weights.

    Uses a min-heap for O(E log V) performance.

    Args:
        n: Number of vertices (0 … n-1).
        edges: List of directed edges (u, v, weight).  Weights must be >= 0.
        start: Source vertex.

    Returns:
        (dist, parent) where dist[v] = shortest distance from start to v
        (INF if unreachable), and parent[v] = predecessor of v on the
        shortest-path tree (-1 for start / unreachable).

    Time:  O(E log V)
    Space: O(V + E)
    """
    # Build adjacency list
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = [INF] * n
    parent = [-1] * n
    dist[start] = 0

    heap = [(0, start)]  # (distance, vertex)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:  # stale entry
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    return dist, parent


def reconstruct_path(parent: List[int], target: int) -> List[int]:
    """
    Reconstruct the shortest path from the parent array returned by dijkstra.

    Args:
        parent: Parent array from dijkstra.
        target: Destination vertex.

    Returns:
        List of vertices from source to target, or [] if unreachable.

    Time: O(V) worst-case
    """
    path = []
    v = target
    while v != -1:
        path.append(v)
        v = parent[v]
    path.reverse()
    if not path or parent[target] == -1 and len(path) == 1:
        return path  # may be just [start] or a full path
    return path


# ======================================================================
# Bellman-Ford
# ======================================================================

def bellman_ford(
    n: int, edges: List[Tuple[int, int, int]], start: int
) -> Tuple[Optional[List[float]], Optional[List[int]], bool]:
    """
    Single-source shortest paths supporting negative edge weights.

    Also detects negative cycles reachable from start.

    Args:
        n: Number of vertices.
        edges: List of (u, v, weight) — can be negative.
        start: Source vertex.

    Returns:
        (dist, parent, has_negative_cycle).  dist[v] = INF if unreachable.
        If a negative cycle is reachable from start, dist and parent are None.

    Time:  O(V * E)
    Space: O(V)
    """
    dist = [INF] * n
    parent = [-1] * n
    dist[start] = 0

    # Relax edges V-1 times
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break  # early exit — no further relaxations possible

    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None, None, True  # negative cycle detected

    return dist, parent, False


# ======================================================================
# Floyd-Warshall
# ======================================================================

def floyd_warshall(
    n: int, edges: List[Tuple[int, int, int]]
) -> Tuple[List[List[float]], Optional[List[List[int]]]]:
    """
    All-pairs shortest paths (Floyd-Warshall).

    Handles negative edges but not negative cycles.

    Args:
        n: Number of vertices.
        edges: List of (u, v, weight).

    Returns:
        (dist, nxt) where dist[i][j] is the shortest distance from i to j,
        and nxt[i][j] is the next vertex on the shortest path from i to j
        (None for unreachable).  If a negative cycle exists, dist is returned
        with at least one diagonal negative entry.

    Time:  O(V^3)
    Space: O(V^2)
    """
    dist: List[List[float]] = [[INF] * n for _ in range(n)]
    nxt: List[List[Optional[int]]] = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
            nxt[u][v] = v

    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[k][j] == INF:
                    continue
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
                    nxt[i][j] = nxt[i][k]

    return dist, nxt


def floyd_path(nxt: List[List[Optional[int]]], u: int, v: int) -> List[int]:
    """Reconstruct the shortest path from Floyd-Warshall next matrix."""
    if nxt[u][v] is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]  # type: ignore[index]
        path.append(u)
    return path


# ======================================================================
# SPFA (Shortest Path Faster Algorithm)
# ======================================================================

def spfa(
    n: int, edges: List[Tuple[int, int, int]], start: int
) -> Tuple[Optional[List[float]], Optional[List[int]], bool]:
    """
    SPFA — a queue-based optimization of Bellman-Ford.

    Works well on sparse graphs; worst-case still O(V*E).

    Args:
        n: Number of vertices.
        edges: List of (u, v, weight).
        start: Source vertex.

    Returns:
        (dist, parent, has_negative_cycle).  dist/None on negative cycle.

    Time:  average O(E), worst O(V*E)
    Space: O(V + E)
    """
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = [INF] * n
    parent = [-1] * n
    in_queue = [False] * n
    cnt = [0] * n  # relaxation count per vertex

    dist[start] = 0
    queue = [start]
    in_queue[start] = True

    while queue:
        u = queue.pop(0)
        in_queue[u] = False

        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True
                    cnt[v] += 1
                    if cnt[v] > n:
                        return None, None, True  # negative cycle

    return dist, parent, False


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # ---------------------------------------------------------------
    # 1. Dijkstra
    # ---------------------------------------------------------------
    # Graph:
    #   0 --1--> 1 (w=4)
    #   0 --2--> 2 (w=2)
    #   1 --3--> 3 (w=5)
    #   2 --4--> 1 (w=1)
    #   2 --5--> 3 (w=8)
    #   3 --6--> 4 (w=3)
    n = 5
    edges_d = [(0, 1, 4), (0, 2, 2), (1, 3, 5), (2, 1, 1), (2, 3, 8), (3, 4, 3)]
    dist_d, parent_d = dijkstra(n, edges_d, 0)
    expected_d = [0, 3, 2, 8, 11]
    if dist_d != expected_d:
        print(f"FAIL dijkstra: expected {expected_d}, got {dist_d}")
        all_pass = False
    path_0_4 = reconstruct_path(parent_d, 4)
    if path_0_4 != [0, 2, 1, 3, 4]:
        print(f"FAIL dijkstra path reconstruction: {path_0_4}")
        all_pass = False

    # ---------------------------------------------------------------
    # 2. Bellman-Ford
    # ---------------------------------------------------------------
    edges_bf = [(0, 1, 1), (1, 2, -3), (0, 2, 4)]
    dist_bf, parent_bf, neg = bellman_ford(3, edges_bf, 0)
    if neg or dist_bf != [0, 1, -2]:
        print(f"FAIL bellman_ford: {dist_bf}, neg={neg}")
        all_pass = False

    # Negative cycle
    edges_neg_cycle = [(0, 1, 1), (1, 2, -3), (2, 0, 1)]
    dist_nc, _, nc = bellman_ford(3, edges_neg_cycle, 0)
    if not nc:
        print(f"FAIL bellman_ford negative cycle detection")
        all_pass = False

    # ---------------------------------------------------------------
    # 3. Floyd-Warshall
    # ---------------------------------------------------------------
    fw_edges = [(0, 1, 3), (0, 2, 8), (1, 2, 2), (1, 3, 1), (2, 1, 4), (3, 2, 7)]
    fw_dist, fw_nxt = floyd_warshall(4, fw_edges)
    if fw_dist[0][3] != 4:  # 0->1->3
        print(f"FAIL floyd_warshall: dist[0][3] = {fw_dist[0][3]}")
        all_pass = False
    fw_path = floyd_path(fw_nxt, 0, 3)
    if fw_path != [0, 1, 3]:
        print(f"FAIL floyd path reconstruction: {fw_path}")
        all_pass = False

    # ---------------------------------------------------------------
    # 4. SPFA
    # ---------------------------------------------------------------
    spfa_dist, spfa_parent, spfa_neg = spfa(n, edges_d, 0)
    if spfa_dist != expected_d:
        print(f"FAIL spfa: expected {expected_d}, got {spfa_dist}")
        all_pass = False
    spfa_nc, _, spfa_nc_flag = spfa(3, edges_neg_cycle, 0)
    if not spfa_nc_flag:
        print(f"FAIL spfa negative cycle detection")
        all_pass = False

    if all_pass:
        print("All shortest path tests PASSED")
    sys.exit(0 if all_pass else 1)
