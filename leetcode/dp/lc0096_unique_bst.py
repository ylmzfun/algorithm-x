"""
LeetCode 96: Unique Binary Search Trees

Given an integer n, return the number of structurally unique BST's
(binary search trees) which has exactly n nodes of unique values
from 1 to n.

Constraints:
- 1 <= n <= 19
"""


class Solution:
    # ── Catalan Number DP O(n²) time, O(n) space ───────────────────────────
    def numTrees(self, n: int) -> int:
        """
        Catalan number: C(n) = sum(C(i-1) * C(n-i)) for i=1..n
        dp[i] = number of unique BSTs with i nodes.
        """
        dp = [0] * (n + 1)
        dp[0] = dp[1] = 1

        for nodes in range(2, n + 1):
            for root in range(1, nodes + 1):
                left = root - 1
                right = nodes - root
                dp[nodes] += dp[left] * dp[right]

        return dp[n]

    # ── Direct Catalan formula O(n) time, O(1) space ───────────────────────
    def numTrees_formula(self, n: int) -> int:
        """C_n = (2n)! / ((n+1)! * n!) = C(2n, n) / (n+1)."""
        import math
        return math.comb(2 * n, n) // (n + 1)


if __name__ == "__main__":
    sol = Solution()
    tests = [
        (1, 1),
        (2, 2),
        (3, 5),
        (4, 14),
        (5, 42),
        (19, 1767263190),
    ]

    for n, expected in tests:
        r1 = sol.numTrees(n)
        r2 = sol.numTrees_formula(n)
        ok = r1 == r2 == expected
        print(f"n={n} → DP={r1}, Formula={r2} | {'✓' if ok else '✗'}")
