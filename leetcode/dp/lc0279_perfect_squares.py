"""
LeetCode 279: Perfect Squares

Given an integer n, return the least number of perfect square numbers
(for example, 1, 4, 9, 16, ...) which sum to n.

Perfect squares are integers that are squares of integers; in other
words, it is the product of some integer with itself.

Constraints:
- 1 <= n <= 10^4
"""

import math
from typing import List


class Solution:
    # ── DP (Coin Change Variant) O(n · √n) time, O(n) space ───────────────
    def numSquares(self, n: int) -> int:
        """dp[i] = min squares summing to i."""
        dp = [float('inf')] * (n + 1)
        dp[0] = 0

        # Precompute squares up to n
        squares = [i * i for i in range(1, int(math.isqrt(n)) + 1)]

        for i in range(1, n + 1):
            for sq in squares:
                if sq > i:
                    break
                dp[i] = min(dp[i], dp[i - sq] + 1)

        return dp[n]

    # ── Lagrange's Four-Square + Legendre's Three-Square Theorems ─────────
    def numSquares_math(self, n: int) -> int:
        """
        Lagrange: every natural number = sum of at most 4 squares.
        Answer is at most 4. Check 1, 2, 4 cases.
        """
        def is_square(x: int) -> bool:
            r = int(math.isqrt(x))
            return r * r == x

        # Case 1: n itself is a perfect square
        if is_square(n):
            return 1

        # Case 4: Legendre: n = 4^a * (8b + 7) → needs 4 squares
        m = n
        while m % 4 == 0:
            m //= 4
        if m % 8 == 7:
            return 4

        # Case 2: sum of two squares
        for i in range(1, int(math.isqrt(n)) + 1):
            if is_square(n - i * i):
                return 2

        # Case 3
        return 3


if __name__ == "__main__":
    sol = Solution()
    tests = [
        (12, 3),   # 4 + 4 + 4
        (13, 2),   # 4 + 9
        (1, 1),
        (4, 1),
        (7, 4),    # Lagrange: 4^0 * (8*0 + 7)
        (28, 4),   # 28 % 4 = 0 -> 7, 7 % 8 = 7 → 4
       ]

    for n, expected in tests:
        r1 = sol.numSquares(n)
        r2 = sol.numSquares_math(n)
        ok = r1 == r2 == expected
        print(f"n={n} → DP={r1}, Math={r2} | {'✓' if ok else '✗'}")
