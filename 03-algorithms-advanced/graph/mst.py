"""
Minimum Spanning Tree (MST) algorithms.

Contains:
- Prim's algorithm (O(E log V) using a min-heap)
- Kruskal's algorithm (O(E log E) using Union-Find)
"""

import heapq
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Union-Find (Disjoint Set Union) — used by Kruskal
# ---------------------------------------------------------------------------

class UnionFind:
    """Disjoint Set Union with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        """
        Initialize n disjoint sets (0 … n-1).

        Args:
            n: Number of elements.

        Time: O(n)
        """
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """
        Find the root of x with path compression.

        Args:
            x: Element index.

        Returns:
            Root of the set containing x.

        Time: O(α(n)) amortized
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union the sets containing x and y (union by rank).

        Args:
            x, y: Element indices.

        Returns:
            True if the sets were merged (x, y were in different sets);
            False if they were already in the same set.

        Time: O(α(n)) amortized
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# ---------------------------------------------------------------------------
# Prim's algorithm
# ---------------------------------------------------------------------------

def prim_mst(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Compute the Minimum Spanning Tree using Prim's algorithm with a min-heap.

    Args:
        n: Number of vertices (0 … n-1).
        edges: List of (u, v, weight) for undirected graph.

    Returns:
        (total_weight, mst_edges) where mst_edges is a list of (u, v, w).

    Time:  O(E log V)
    Space: O(V + E)
    """
    # Build adjacency list
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = [False] * n
    min_heap: List[Tuple[int, int, int]] = []  # (weight, to, from)
    mst_edges: List[Tuple[int, int, int]] = []
    total_weight = 0

    # Start from vertex 0
    visited[0] = True
    for v, w in adj[0]:
        heapq.heappush(min_heap, (w, v, 0))

    while min_heap:
        w, u, prev = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True
        total_weight += w
        mst_edges.append((prev, u, w))

        for v, weight in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (weight, v, u))

    return total_weight, mst_edges


# ---------------------------------------------------------------------------
# Kruskal's algorithm
# ---------------------------------------------------------------------------

def kruskal_mst(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Compute the Minimum Spanning Tree using Kruskal's algorithm with Union-Find.

    Args:
        n: Number of vertices (0 … n-1).
        edges: List of (u, v, weight) for undirected graph.

    Returns:
        (total_weight, mst_edges) where mst_edges is a list of (u, v, w).

    Time:  O(E log E)
    Space: O(V + E)
    """
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(n)
    mst_edges: List[Tuple[int, int, int]] = []
    total_weight = 0

    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == n - 1:
                break

    return total_weight, mst_edges


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    all_pass = True

    # ---------- Shared test graph ----------
    # Graph from CLRS example:
    #   (0)---4---(1)
    #    | \     / |
    #    2  8   7  9
    #    |   \ /   |
    #   (2)---1---(3)
    #
    n = 4
    edges = [
        (0, 1, 4), (0, 2, 2), (0, 3, 8),
        (1, 2, 7), (1, 3, 9),
        (2, 3, 1),
    ]

    # --- Prim ---
    w_prim, mst_prim = prim_mst(n, edges)
    prim_ok = (w_prim == 7 and len(mst_prim) == n - 1)
    if not prim_ok:
        print(f"FAIL prim_mst: got weight={w_prim}, edges={mst_prim}")
        all_pass = False

    # --- Kruskal ---
    w_kru, mst_kru = kruskal_mst(n, edges)
    kru_ok = (w_kru == 7 and len(mst_kru) == n - 1)
    if not kru_ok:
        print(f"FAIL kruskal_mst: got weight={w_kru}, edges={mst_kru}")
        all_pass = False

    # --- Both algorithms must agree on total weight ---
    if w_prim != w_kru:
        print(f"FAIL weight mismatch: prim={w_prim}, kruskal={w_kru}")
        all_pass = False

    # --- Single-node graph ---
    w1, e1 = prim_mst(1, [])
    if w1 != 0 or e1 != []:
        print(f"FAIL single-node")
        all_pass = False

    # --- Disconnected graph (Kruskal simply returns a forest) ---
    edges_disconnected = [(0, 1, 5), (2, 3, 3)]
    w_dis, mst_dis = kruskal_mst(4, edges_disconnected)
    if w_dis != 8 or len(mst_dis) != 2:
        print(f"FAIL disconnected kruskal: got weight={w_dis}, edges={mst_dis}")
        all_pass = False

    if all_pass:
        print("All MST tests PASSED")
    sys.exit(0 if all_pass else 1)
