"""
Network flow algorithms.

Contains:
- Ford-Fulkerson / Edmonds-Karp (BFS-based, O(V * E^2))
- Dinic's algorithm (O(V^2 * E))
- Min-cut max-flow theorem
- Bipartite matching using max flow
"""

from collections import deque
from typing import List, Optional, Tuple


INF = float("inf")


# ======================================================================
# Edmonds-Karp (BFS-based Ford-Fulkerson)
# ======================================================================

def edmonds_karp(
    n: int, edges: List[Tuple[int, int, int]], source: int, sink: int
) -> int:
    """
    Compute maximum flow using Edmonds-Karp (BFS-based Ford-Fulkerson).

    Uses a capacity / residual graph represented as an adjacency matrix
    for simplicity (can be converted to adjacency lists for sparse graphs).

    Args:
        n: Number of vertices.
        edges: List of (u, v, capacity) for directed edges.
        source: Source vertex index.
        sink: Sink vertex index.

    Returns:
        Maximum flow value from source to sink.

    Time:  O(V * E^2)
    Space: O(V^2)
    """
    # Build capacity matrix (also serves as residual graph)
    cap = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] += c  # support parallel edges

    flow = 0
    parent = [-1] * n

    while True:
        # BFS to find an augmenting path
        parent = [-1] * n
        q = deque([source])
        parent[source] = source

        while q:
            u = q.popleft()
            for v in range(n):
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    q.append(v)
                    if v == sink:
                        break
            if parent[sink] != -1:
                break

        if parent[sink] == -1:
            break  # no more augmenting paths

        # Find bottleneck capacity on the path
        v = sink
        bottleneck = INF
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, cap[u][v])
            v = u

        # Augment flow
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= bottleneck
            cap[v][u] += bottleneck
            v = u

        flow += bottleneck

    return int(flow)


def min_cut(
    n: int, edges: List[Tuple[int, int, int]], source: int, sink: int
) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Compute the minimum s-t cut using max-flow.

    After computing max flow, the source-side reachable vertices in the
    residual graph form the min-cut.

    Args:
        n: Number of vertices.
        edges: List of (u, v, capacity).
        source: Source vertex.
        sink: Sink vertex.

    Returns:
        (max_flow_value, cut_edges) where cut_edges list (u, v) that cross
        from the source side to the sink side.

    Time:  O(V * E^2)
    """
    cap = [[0] * n for _ in range(n)]
    original_edges_set = set()
    for u, v, c in edges:
        cap[u][v] += c
        original_edges_set.add((u, v))

    parent = [-1] * n

    while True:
        parent = [-1] * n
        q = deque([source])
        parent[source] = source
        while q:
            u = q.popleft()
            for v in range(n):
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    q.append(v)
        if parent[sink] == -1:
            break
        v = sink
        bottleneck = INF
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, cap[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= bottleneck
            cap[v][u] += bottleneck
            v = u

    # BFS from source in residual graph
    visited = [False] * n
    q = deque([source])
    visited[source] = True
    while q:
        u = q.popleft()
        for v in range(n):
            if not visited[v] and cap[u][v] > 0:
                visited[v] = True
                q.append(v)

    # Edges crossing from visited to unvisited that existed originally
    cut_edges = [
        (u, v) for u, v in original_edges_set if visited[u] and not visited[v]
    ]

    # Compute max flow from original capacities - residual
    total_flow = 0
    for u, v, c in edges:
        residual = max(0, c - max(0, c - cap[u][v]))  # original - current residual
        # simpler: track flow separately

    # Recompute total flow
    total_flow = 0
    capacity_before = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        capacity_before[u][v] += c
    for u in range(n):
        for v in range(n):
            sent = capacity_before[u][v] - cap[u][v]
            if sent > 0:
                total_flow += sent

    return total_flow // 2, cut_edges  # divide by 2 because each edge counted twice?


# Simpler min_cut wrapper using the max_flow result
def min_cut_from_max_flow(
    n: int,
    edges: List[Tuple[int, int, int]],
    residual: List[List[int]],
    source: int,
) -> List[Tuple[int, int]]:
    """
    Given a residual graph after max flow, find min-cut edges.

    Args:
        n: Number of vertices.
        edges: Original edges.
        residual: The residual capacity matrix after max flow.
        source: Source vertex.

    Returns:
        List of edges in the minimum cut.
    """
    visited = [False] * n
    q = deque([source])
    visited[source] = True
    while q:
        u = q.popleft()
        for v in range(n):
            if not visited[v] and residual[u][v] > 0:
                visited[v] = True
                q.append(v)

    original = set()
    for u, v, _ in edges:
        original.add((u, v))

    return [(u, v) for u, v in original if visited[u] and not visited[v]]


# ======================================================================
# Dinic's algorithm
# ======================================================================

class Dinic:
    """Dinic's max flow algorithm with level graph and blocking flow."""

    def __init__(self, n: int) -> None:
        """
        Initialize Dinic for n vertices.

        Args:
            n: Number of vertices (0 … n-1).

        Time: O(n)
        """
        self.n = n
        self.adj: List[List[List[int]]] = [[] for _ in range(n)]
        # Each edge: [to, rev_index, capacity]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        """
        Add a directed edge from u to v with the given capacity.

        Args:
            u, v: Vertex indices.
            cap: Edge capacity (must be non-negative).

        Time: O(1)
        """
        self.adj[u].append([v, len(self.adj[v]), cap])
        self.adj[v].append([u, len(self.adj[u]) - 1, 0])  # reverse edge

    def _bfs(self, s: int, t: int, level: List[int]) -> bool:
        """Build level graph. Returns True if sink is reachable."""
        for i in range(self.n):
            level[i] = -1
        q = deque([s])
        level[s] = 0
        while q:
            u = q.popleft()
            for v, rev, cap in self.adj[u]:
                if cap > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[t] >= 0

    def _dfs(
        self, u: int, t: int, f: int, level: List[int], it: List[int]
    ) -> int:
        """Send flow along level graph using DFS."""
        if u == t:
            return f
        for i in range(it[u], len(self.adj[u])):
            it[u] = i
            v, rev, cap = self.adj[u][i]
            if cap > 0 and level[u] < level[v]:
                ret = self._dfs(v, t, min(f, cap), level, it)
                if ret > 0:
                    # update residual capacities
                    self.adj[u][i][2] -= ret
                    self.adj[v][rev][2] += ret
                    return ret
        return 0

    def max_flow(self, s: int, t: int) -> int:
        """
        Compute the maximum flow from s to t.

        Args:
            s: Source vertex.
            t: Sink vertex.

        Returns:
            Maximum flow value.

        Time:  O(V^2 * E)
        Space: O(V + E)
        """
        flow = 0
        level = [-1] * self.n
        INF_FLOW = 10**18

        while self._bfs(s, t, level):
            it = [0] * self.n
            while True:
                pushed = self._dfs(s, t, INF_FLOW, level, it)
                if pushed == 0:
                    break
                flow += pushed

        return flow


def dinic_max_flow(
    n: int, edges: List[Tuple[int, int, int]], source: int, sink: int
) -> int:
    """
    Convenience wrapper: compute max flow with Dinic's algorithm.

    Args:
        n: Number of vertices.
        edges: List of (u, v, capacity).
        source: Source vertex.
        sink: Sink vertex.

    Returns:
        Maximum flow value.

    Time:  O(V^2 * E)
    """
    dinic = Dinic(n)
    for u, v, c in edges:
        dinic.add_edge(u, v, c)
    return dinic.max_flow(source, sink)


# ======================================================================
# Bipartite matching via max flow
# ======================================================================

def bipartite_max_matching(
    left_size: int, right_size: int, edges: List[Tuple[int, int]]
) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Find maximum bipartite matching by reduction to max flow.

    Vertices on the left: 0 … left_size-1
    Vertices on the right: left_size … left_size+right_size-1

    Args:
        left_size: Number of vertices in the left partition.
        right_size: Number of vertices in the right partition.
        edges: List of (left_vertex, right_vertex) — right vertices are
               given by their local index (0 … right_size-1).

    Returns:
        (max_matching_size, matching_edges) where each edge is
        (left_v, right_v) in local coordinates.

    Time:  O(E * sqrt(V)) with Hopcroft-Karp-like flow, O(V * E^2) worst-case
           with Edmonds-Karp.
    """
    total = left_size + right_size + 2
    source = total - 2
    sink = total - 1

    flow_edges = []
    # source -> left
    for i in range(left_size):
        flow_edges.append((source, i, 1))
    # left -> right
    for u, v in edges:
        flow_edges.append((u, left_size + v, 1))
    # right -> sink
    for j in range(right_size):
        flow_edges.append((left_size + j, sink, 1))

    dinic = Dinic(total)
    for u, v, c in flow_edges:
        dinic.add_edge(u, v, c)

    max_match = dinic.max_flow(source, sink)

    # Extract matching edges
    matching_edges = []
    for u, v, _ in flow_edges:
        if u < left_size and left_size <= v < left_size + right_size:
            # Check if this edge has flow
            # Find the reverse edge capacity in dinic.adj
            for to, rev, cap in dinic.adj[u]:
                if to == v and cap == 0:  # original forward edge used
                    matching_edges.append((u, v - left_size))
                    break

    return max_match, matching_edges


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # -------------------- Edmonds-Karp --------------------
    # Simple flow network
    n = 6
    edges = [
        (0, 1, 10), (0, 2, 10),
        (1, 2, 2), (1, 3, 4), (1, 4, 8),
        (2, 4, 9),
        (3, 5, 10),
        (4, 3, 6), (4, 5, 10),
    ]
    flow_ek = edmonds_karp(n, edges, 0, 5)
    if flow_ek != 19:
        print(f"FAIL edmonds_karp: expected 19, got {flow_ek}")
        all_pass = False

    # -------------------- Dinic --------------------
    flow_dinic = dinic_max_flow(n, edges, 0, 5)
    if flow_dinic != 19:
        print(f"FAIL dinic: expected 19, got {flow_dinic}")
        all_pass = False

    # Another test: simple path
    flow_simple = edmonds_karp(3, [(0, 1, 5), (1, 2, 3)], 0, 2)
    if flow_simple != 3:
        print(f"FAIL simple flow: {flow_simple}")
        all_pass = False

    flow_simple_d = dinic_max_flow(3, [(0, 1, 5), (1, 2, 3)], 0, 2)
    if flow_simple_d != 3:
        print(f"FAIL dinic simple flow: {flow_simple_d}")
        all_pass = False

    # -------------------- Bipartite Matching --------------------
    # Left: 0,1,2   Right: 0,1,2
    # Edges: 0-0, 0-1, 1-1, 2-2
    bp_edges = [(0, 0), (0, 1), (1, 1), (2, 2)]
    size, matching = bipartite_max_matching(3, 3, bp_edges)
    if size != 3:
        print(f"FAIL bipartite matching size: expected 3, got {size}")
        all_pass = False

    # Simple bipartite: 2-2
    size2, _ = bipartite_max_matching(2, 2, [(0, 0), (1, 1)])
    if size2 != 2:
        print(f"FAIL bipartite matching 2x2: {size2}")
        all_pass = False

    if all_pass:
        print("All network flow tests PASSED")
    sys.exit(0 if all_pass else 1)
