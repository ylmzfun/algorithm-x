"""
LeetCode 70: Climbing Stairs

You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct
ways can you climb to the top?

Constraints:
- 1 <= n <= 45
"""


class Solution:
    # ── Fibonacci DP O(n) time, O(1) space ────────────────────────────────
    def climbStairs(self, n: int) -> int:
        """dp[i] = dp[i-1] + dp[i-2] (Fibonacci)."""
        if n <= 2:
            return n

        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            prev2, prev1 = prev1, prev1 + prev2

        return prev1

    # ── Matrix Exponentiation O(log n) time ────────────────────────────────
    def climbStairs_matrix(self, n: int) -> int:
        """Using fast matrix exponentiation for Fibonacci."""
        if n <= 2:
            return n

        def multiply(a, b):
            return [
                [a[0][0] * b[0][0] + a[0][1] * b[1][0],
                 a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                [a[1][0] * b[0][0] + a[1][1] * b[1][0],
                 a[1][0] * b[0][1] + a[1][1] * b[1][1]],
            ]

        def power(mat, exp):
            res = [[1, 0], [0, 1]]
            while exp:
                if exp & 1:
                    res = multiply(res, mat)
                mat = multiply(mat, mat)
                exp >>= 1
            return res

        base = [[1, 1], [1, 0]]
        result = power(base, n)
        return result[0][0]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        (2, 2),
        (3, 3),
        (4, 5),
        (5, 8),
        (10, 89),
        (45, 1836311903),
    ]

    for n, expected in tests:
        r1 = sol.climbStairs(n)
        r2 = sol.climbStairs_matrix(n)
        ok = r1 == r2 == expected
        print(f"n={n} → DP={r1}, Matrix={r2} | {'✓' if ok else '✗'}")
