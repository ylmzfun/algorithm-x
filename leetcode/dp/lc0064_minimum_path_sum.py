"""
LeetCode 64: Minimum Path Sum

Given a m x n grid filled with non-negative numbers, find a path from
top left to bottom right, which minimizes the sum of all numbers along
its path. You can only move either down or right at any point in time.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 200
- 0 <= grid[i][j] <= 200
"""

from typing import List


class Solution:
    # ── 2D DP → 1D optimization O(m·n) time, O(n) space ────────────────────
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [0] * n

        dp[0] = grid[0][0]
        for j in range(1, n):
            dp[j] = dp[j - 1] + grid[0][j]

        for i in range(1, m):
            dp[0] += grid[i][0]
            for j in range(1, n):
                dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]

        return dp[-1]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
        ([[1, 2, 3], [4, 5, 6]], 12),
        ([[1, 2], [1, 1]], 3),
        ([[5]], 5),
        ([[1, 100], [1, 1], [1, 1]], 4),
    ]

    for grid, expected in tests:
        result = sol.minPathSum(grid)
        status = "✓" if result == expected else "✗"
        print(f"{grid} → {result} (expected {expected}) {status}")
