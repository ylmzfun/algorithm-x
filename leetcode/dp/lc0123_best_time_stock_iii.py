"""
LeetCode 123: Best Time to Buy and Sell Stock III

You are given an array prices where prices[i] is the price of a given
stock on the i-th day. Find the maximum profit you can achieve.
You may complete at most two transactions.

Note: You may not engage in multiple transactions simultaneously
(i.e., you must sell the stock before you buy again).

Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^5
"""

from typing import List


class Solution:
    # ── State Machine DP O(n) time, O(1) space ────────────────────────────
    def maxProfit(self, prices: List[int]) -> int:
        """
        States:
        buy1  = max profit after 1st buy  (spent money)
        sell1 = max profit after 1st sell (earned money)
        buy2  = max profit after 2nd buy
        sell2 = max profit after 2nd sell
        """
        buy1 = buy2 = float('-inf')
        sell1 = sell2 = 0

        for price in prices:
            buy1 = max(buy1, -price)
            sell1 = max(sell1, buy1 + price)
            buy2 = max(buy2, sell1 - price)
            sell2 = max(sell2, buy2 + price)

        return sell2

    # ── DP with two arrays O(n) time, O(n) space ──────────────────────────
    def maxProfit_2arrays(self, prices: List[int]) -> int:
        """Max profit by splitting at each day: left max + right max."""
        n = len(prices)
        if n < 2:
            return 0

        # left[i] = max profit with one transaction in prices[:i+1]
        left = [0] * n
        min_price = prices[0]
        for i in range(1, n):
            left[i] = max(left[i - 1], prices[i] - min_price)
            min_price = min(min_price, prices[i])

        # right[i] = max profit with one transaction in prices[i:]
        right = [0] * n
        max_price = prices[-1]
        for i in range(n - 2, -1, -1):
            right[i] = max(right[i + 1], max_price - prices[i])
            max_price = max(max_price, prices[i])

        return max(left[i] + right[i] for i in range(n))


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([3, 3, 5, 0, 0, 3, 1, 4], 6),
        ([1, 2, 3, 4, 5], 4),
        ([7, 6, 4, 3, 1], 0),
        ([1], 0),
        ([1, 2, 4, 2, 5, 7, 2, 4, 9, 0], 13),
    ]

    for prices, expected in tests:
        r1 = sol.maxProfit(prices)
        r2 = sol.maxProfit_2arrays(prices)
        ok = r1 == r2 == expected
        print(f"{prices} → StateDP={r1}, Split={r2} | {'✓' if ok else '✗'}")
