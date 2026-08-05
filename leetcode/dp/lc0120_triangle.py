"""
LeetCode 120: Triangle

Given a triangle array, return the minimum path sum from top to bottom.
For each step, you may move to an adjacent number of the row below.
More formally, if you are on index i on the current row, you may move
to either index i or index i + 1 on the next row.

Constraints:
- 1 <= triangle.length <= 200
- triangle[0].length == 1
- triangle[i].length == triangle[i-1].length + 1
- -10^4 <= triangle[i][j] <= 10^4
"""

from typing import List


class Solution:
    # ── Bottom-Up DP O(n²) time, O(n) space ────────────────────────────────
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        """Start from the bottom row and propagate minimums upward."""
        n = len(triangle)
        dp = triangle[-1][:]  # start with last row

        for row in range(n - 2, -1, -1):
            for col in range(len(triangle[row])):
                dp[col] = triangle[row][col] + min(dp[col], dp[col + 1])

        return dp[0]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]], 11),
        ([[-10]], -10),
        ([[1], [2, 3]], 3),
        ([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3], [1, 2, 3, 4, 5]], 13),
    ]

    for triangle, expected in tests:
        result = sol.minimumTotal(triangle)
        status = "✓" if result == expected else "✗"
        print(f"{triangle} → {result} (expected {expected}) {status}")
