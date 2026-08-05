"""
LeetCode 343: Integer Break

Given an integer n, break it into the sum of k positive integers,
where k >= 2, and maximize the product of those integers.

Return the maximum product you can get.

Constraints:
- 2 <= n <= 58
"""


class Solution:
    # ── DP O(n²) time, O(n) space ────────────────────────────────────────
    def integerBreak(self, n: int) -> int:
        """dp[i] = max product for integer i."""
        if n <= 3:
            return n - 1  # 2→1, 3→2

        dp = [0] * (n + 1)
        dp[2] = 2
        dp[3] = 3

        for i in range(4, n + 1):
            # Try splitting into j and i-j
            dp[i] = max(dp[j] * dp[i - j] for j in range(2, i // 2 + 1))

        return dp[n]

    # ── Math O(1) time, O(1) space ───────────────────────────────────────
    def integerBreak_math(self, n: int) -> int:
        """
        Optimal: use as many 3's as possible, then handle remainder.
        If remainder is 1, convert one 3 to 2+2 (since 3*1 < 2*2).
        """
        if n <= 3:
            return n - 1

        quotient, remainder = divmod(n, 3)
        if remainder == 0:
            return 3 ** quotient
        elif remainder == 1:
            return 3 ** (quotient - 1) * 4
        else:  # remainder == 2
            return 3 ** quotient * 2


if __name__ == "__main__":
    sol = Solution()
    tests = [
        (2, 1),
        (3, 2),
        (4, 4),
        (5, 6),
        (6, 9),
        (10, 36),
        (58, 1549681956),
    ]

    for n, expected in tests:
        r1 = sol.integerBreak(n)
        r2 = sol.integerBreak_math(n)
        ok = r1 == r2 == expected
        print(f"n={n} → DP={r1}, Math={r2} | {'✓' if ok else '✗'}")
