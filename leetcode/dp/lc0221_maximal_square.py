"""
LeetCode 221: Maximal Square

Given an m x n binary matrix filled with 0's and 1's, find the largest
square containing only 1's and return its area.

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 300
- matrix[i][j] is '0' or '1'.
"""

from typing import List


class Solution:
    # ── 2D DP O(m·n) time, O(n) space ─────────────────────────────────────
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        """
        dp[i][j] = side length of largest square ending at (i,j).
        dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
        Space optimized to one row + one variable for diagonal.
        """
        m, n = len(matrix), len(matrix[0])
        dp = [0] * (n + 1)
        max_side = 0
        prev = 0  # dp[i-1][j-1]

        for i in range(m):
            for j in range(n):
                temp = dp[j + 1]
                if matrix[i][j] == '1':
                    dp[j + 1] = min(dp[j], dp[j + 1], prev) + 1
                    max_side = max(max_side, dp[j + 1])
                else:
                    dp[j + 1] = 0
                prev = temp

        return max_side * max_side


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([["1", "0", "1", "0", "0"],
          ["1", "0", "1", "1", "1"],
          ["1", "1", "1", "1", "1"],
          ["1", "0", "0", "1", "0"]], 4),
        ([["0", "1"], ["1", "0"]], 1),
        ([["0"]], 0),
        ([["1"]], 1),
        ([["1", "1"], ["1", "1"]], 4),
    ]

    for matrix, expected in tests:
        result = sol.maximalSquare(matrix)
        status = "✓" if result == expected else "✗"
        print(f"area={result} (expected {expected}) {status}")
