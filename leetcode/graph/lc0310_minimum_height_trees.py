"""
310. Minimum Height Trees
https://leetcode.com/problems/minimum-height-trees/

A tree is an undirected graph in which any two vertices are connected by
exactly one path. Given a tree with n nodes labeled from 0 to n-1 and an
array of n-1 edges, return a list of all MHT root labels.

The height of a rooted tree is the number of edges on the longest downward
path between the root and a leaf.
"""

from __future__ import annotations
from collections import defaultdict, deque


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Topological Peeling (Kahn's-like on undirected tree)
# Intuition: The MHT roots are the centroids of the tree.
# Peel leaves layer by layer until ≤2 nodes remain.
# Time: O(N)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def find_min_height_trees(n: int, edges: list[list[int]]) -> list[int]:
    """Find all MHT roots by topological peeling."""
    if n == 1:
        return [0]

    adj: dict[int, set[int]] = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    # Start with all leaves (degree == 1)
    leaves: deque[int] = deque(u for u in range(n) if len(adj[u]) == 1)
    remaining = n

    # Peel leaves until ≤2 nodes remain
    while remaining > 2:
        size = len(leaves)
        remaining -= size
        for _ in range(size):
            leaf = leaves.popleft()
            neighbor = adj[leaf].pop()  # leaf has exactly one neighbor
            adj[neighbor].discard(leaf)
            if len(adj[neighbor]) == 1:
                leaves.append(neighbor)

    return list(leaves)


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, n: int, edges: list[list[int]], expected: list[int]):
        result = find_min_height_trees(n, edges)
        ok = sorted(result) == sorted(expected)
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", 4, [[1, 0], [1, 2], [1, 3]], [1])
    test("Example 2", 6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]], [3, 4])
    test("Single node", 1, [], [0])
    print("\nAll minimum height trees tests completed.")
