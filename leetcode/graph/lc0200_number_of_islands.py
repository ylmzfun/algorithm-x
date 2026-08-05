"""
200. Number of Islands
https://leetcode.com/problems/number-of-islands/

Given an m x n 2D binary grid `grid` which represents a map of '1's (land) and
'0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands
horizontally or vertically.
"""

from __future__ import annotations
from collections import deque
from typing import Union


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: DFS (recursive)
# Time: O(M × N) — visit each cell at most once.
# Space: O(M × N) worst-case recursion depth (all land).
# ──────────────────────────────────────────────────────────────────────────────
def num_islands_dfs(grid: list[list[str]]) -> int:
    """Count islands by sinking visited land with DFS."""
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # sink
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)
                count += 1
    return count


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: BFS (iterative)
# Time: O(M × N)
# Space: O(min(M, N)) — queue size bound.
# ──────────────────────────────────────────────────────────────────────────────
def num_islands_bfs(grid: list[list[str]]) -> int:
    """Count islands by sinking visited land with BFS."""
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def bfs(r: int, c: int) -> None:
        q: deque[tuple[int, int]] = deque([(r, c)])
        grid[r][c] = "0"
        while q:
            cr, cc = q.popleft()
            for dr, dc in dirs:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    grid[nr][nc] = "0"
                    q.append((nr, nc))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                bfs(r, c)
                count += 1
    return count


# ──────────────────────────────────────────────────────────────────────────────
# Approach 3: Union-Find (Disjoint Set Union)
# Time: O(M × N × α(M×N)) ≈ O(M × N)
# Space: O(M × N)
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


def num_islands_uf(grid: list[list[str]]) -> int:
    """Count islands using Union-Find."""
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    dsu = DSU(rows * cols)
    water_count = 0
    dirs = ((1, 0), (0, 1))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if nr < rows and nc < cols and grid[nr][nc] == "1":
                        dsu.union(r * cols + c, nr * cols + nc)
            else:
                water_count += 1

    return dsu.count - water_count


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import copy

    def test(label: str, grid: list[list[str]], expected: int):
        methods = [
            ("DFS", num_islands_dfs),
            ("BFS", num_islands_bfs),
            ("UF", num_islands_uf),
        ]
        for name, fn in methods:
            g = copy.deepcopy(grid)
            result = fn(g)
            ok = result == expected
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ], 1)

    test("Example 2", [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ], 3)

    test("Empty", [], 0)
    print("\nAll number of islands tests completed.")
