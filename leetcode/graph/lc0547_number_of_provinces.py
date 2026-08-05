"""
547. Number of Provinces
https://leetcode.com/problems/number-of-provinces/

There are n cities. Some of them are connected, while some are not.
Given an n x n matrix `isConnected` where isConnected[i][j] = 1 if the i-th
city and the j-th city are directly connected, and isConnected[i][j] = 0
otherwise.

A province is a group of directly or indirectly connected cities.
Return the total number of provinces.
"""

from __future__ import annotations
from collections import deque


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Union-Find
# Time: O(N² × α(N)) ≈ O(N²)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
class DSU:
    __slots__ = ("parent", "rank", "count")
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        if self.rank[xr] < self.rank[yr]:
            xr, yr = yr, xr
        self.parent[yr] = xr
        if self.rank[xr] == self.rank[yr]:
            self.rank[xr] += 1
        self.count -= 1


def find_circle_num_uf(is_connected: list[list[int]]) -> int:
    """Union-Find on the upper triangle of the adjacency matrix."""
    n = len(is_connected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    return dsu.count


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: DFS
# Time: O(N²)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def find_circle_num_dfs(is_connected: list[list[int]]) -> int:
    """DFS to mark all cities in the same province."""
    n = len(is_connected)
    visited = [False] * n

    def dfs(city: int) -> None:
        visited[city] = True
        for neighbor, connected in enumerate(is_connected[city]):
            if connected and not visited[neighbor]:
                dfs(neighbor)

    provinces = 0
    for city in range(n):
        if not visited[city]:
            dfs(city)
            provinces += 1
    return provinces


# ──────────────────────────────────────────────────────────────────────────────
# Approach 3: BFS
# Time: O(N²)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def find_circle_num_bfs(is_connected: list[list[int]]) -> int:
    """BFS to mark all cities in the same province."""
    n = len(is_connected)
    visited = [False] * n
    provinces = 0

    for city in range(n):
        if not visited[city]:
            provinces += 1
            q: deque[int] = deque([city])
            visited[city] = True
            while q:
                cur = q.popleft()
                for nxt, conn in enumerate(is_connected[cur]):
                    if conn and not visited[nxt]:
                        visited[nxt] = True
                        q.append(nxt)

    return provinces


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, graph: list[list[int]], expected: int):
        methods = [
            ("UF", find_circle_num_uf),
            ("DFS", find_circle_num_dfs),
            ("BFS", find_circle_num_bfs),
        ]
        for name, fn in methods:
            result = fn(graph)
            ok = result == expected
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2)
    test("Example 2", [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3)
    test("Single city", [[1]], 1)
    print("\nAll number of provinces tests completed.")
