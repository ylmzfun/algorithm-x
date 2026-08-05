"""
684. Redundant Connection
https://leetcode.com/problems/redundant-connection/

In this problem, a tree is an undirected graph that is connected and has no
cycles. You are given a graph that started as a tree with n nodes labeled
from 1 to n, with one additional edge added. Return an edge that can be
removed so that the resulting graph is a tree. If there are multiple answers,
return the answer that occurs last in the input.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Union-Find
# The redundant edge is the first edge whose endpoints are already in the
# same component. Process edges in order and return the one that forms a cycle.
# Time: O(N × α(N)) ≈ O(N)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    """Return the redundant edge using Union-Find."""
    n = len(edges)
    parent = list(range(n + 1))
    rank = [0] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> bool:
        """Return False if x and y are already in the same component."""
        xr, yr = find(x), find(y)
        if xr == yr:
            return False
        if rank[xr] < rank[yr]:
            xr, yr = yr, xr
        parent[yr] = xr
        if rank[xr] == rank[yr]:
            rank[xr] += 1
        return True

    for u, v in edges:
        if not union(u, v):
            return [u, v]

    return []  # unreachable


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, edges: list[list[int]], expected: list[int]):
        result = find_redundant_connection(edges)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [[1, 2], [1, 3], [2, 3]], [2, 3])
    test("Example 2", [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]], [1, 4])
    test("Five nodes", [[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]], [4, 1])
    print("\nAll redundant connection tests completed.")
