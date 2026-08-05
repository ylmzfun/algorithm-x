"""
LeetCode 62: Unique Paths

There is a robot on an m x n grid. The robot is initially located at
the top-left corner (grid[0][0]). The robot tries to move to the
bottom-right corner (grid[m-1][n-1]). The robot can only move either
down or right at any point in time.

Given the two integers m and n, return the number of possible unique
paths that the robot can take to reach the bottom-right corner.

Constraints:
- 1 <= m, n <= 100
"""


class Solution:
    # ── Approach 1: 2D DP O(m·n) time, O(m·n) space ────────────────────────
    def uniquePaths_2d(self, m: int, n: int) -> int:
        """Classic 2D DP table."""
        dp = [[1] * n for _ in range(m)]  # first row/col are all 1

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m - 1][n - 1]

    # ── Approach 2: 1D DP O(m·n) time, O(n) space ─────────────────────────
    def uniquePaths_1d(self, m: int, n: int) -> int:
        """Space-optimized: only keep one row."""
        dp = [1] * n

        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]

        return dp[-1]

    # ── Approach 3: Combinatorics O(min(m,n)) time, O(1) space ─────────────
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Total steps = (m-1) down + (n-1) right = m+n-2 steps.
        Choose (m-1) down steps (or (n-1) right steps).
        C(m+n-2, m-1) = C(m+n-2, n-1).
        """
        import math
        return math.comb(m + n - 2, m - 1)


if __name__ == "__main__":
    sol = Solution()
    tests = [
        (3, 7, 28),
        (3, 2, 3),
        (1, 1, 1),
        (10, 10, 48620),
        (2, 100, 100),
    ]

    for m, n, expected in tests:
        r1 = sol.uniquePaths_2d(m, n)
        r2 = sol.uniquePaths_1d(m, n)
        r3 = sol.uniquePaths(m, n)
        ok = r1 == r2 == r3 == expected
        print(f"({m},{n}) → 2D={r1}, 1D={r2}, Comb={r3} | {'✓' if ok else '✗'}")
