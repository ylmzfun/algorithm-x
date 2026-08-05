"""
LeetCode 63: Unique Paths II

You are given an m x n integer array grid. There is a robot initially
located at the top-left corner. The robot tries to move to the
bottom-right corner. The robot can only move either down or right.

An obstacle and space are marked as 1 and 0 respectively in grid.
A path that the robot takes cannot include any square that is an
obstacle. Return the number of possible unique paths.

Constraints:
- m == obstacleGrid.length
- n == obstacleGrid[i].length
- 1 <= m, n <= 100
- obstacleGrid[i][j] is 0 or 1.
"""

from typing import List


class Solution:
    # ── 2D DP → 1D optimization O(m·n) time, O(n) space ────────────────────
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])

        # If start or end is blocked
        if obstacleGrid[0][0] == 1 or obstacleGrid[m - 1][n - 1] == 1:
            return 0

        dp = [0] * n
        dp[0] = 1  # start

        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0
                elif j > 0:
                    dp[j] += dp[j - 1]

        return dp[-1]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2),
        ([[0, 1], [0, 0]], 1),
        ([[1, 0]], 0),
        ([[0, 0], [0, 0]], 2),
        ([[0, 0], [1, 1], [0, 0]], 0),
        ([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]], 4),
    ]

    for grid, expected in tests:
        result = sol.uniquePathsWithObstacles(grid)
        status = "✓" if result == expected else "✗"
        print(f"{grid} → {result} (expected {expected}) {status}")
