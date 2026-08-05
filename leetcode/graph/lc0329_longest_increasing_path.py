"""
329. Longest Increasing Path in a Matrix
https://leetcode.com/problems/longest-increasing-path-in-a-matrix/

Given an m x n integers matrix, return the length of the longest increasing
path in the matrix. From each cell, you can move in four directions: left,
right, up, down. You may not move diagonally or move outside the boundary.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: DFS with Memoization
# Time: O(M × N) — each cell visited once; cache ensures single computation.
# Space: O(M × N) — cache matrix + recursion depth.
# ──────────────────────────────────────────────────────────────────────────────
def longest_increasing_path(matrix: list[list[int]]) -> int:
    """DFS + memo: from each cell, explore only larger neighbors."""
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    cache = [[0] * cols for _ in range(rows)]
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def dfs(r: int, c: int) -> int:
        if cache[r][c]:
            return cache[r][c]

        max_path = 1
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                max_path = max(max_path, 1 + dfs(nr, nc))

        cache[r][c] = max_path
        return max_path

    return max(dfs(r, c) for r in range(rows) for c in range(cols))


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, matrix: list[list[int]], expected: int):
        result = longest_increasing_path(matrix)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [
        [9, 9, 4],
        [6, 6, 8],
        [2, 1, 1],
    ], 4)  # 1→2→6→9

    test("Example 2", [
        [3, 4, 5],
        [3, 2, 6],
        [2, 2, 1],
    ], 4)  # 3→4→5→6 or 1→2→3→4

    test("Single cell", [[5]], 1)
    print("\nAll longest increasing path tests completed.")
