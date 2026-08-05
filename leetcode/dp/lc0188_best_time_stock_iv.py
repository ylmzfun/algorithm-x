"""
LeetCode 188: Best Time to Buy and Sell Stock IV

You are given an integer array prices where prices[i] is the price of
a given stock on the i-th day, and an integer k. Find the maximum
profit you can achieve. You may complete at most k transactions: i.e.
you may buy at most k times and sell at most k times.

Note: You may not engage in multiple transactions simultaneously
(i.e., you must sell the stock before you buy again).

Constraints:
- 1 <= k <= 100
- 1 <= prices.length <= 1000
- 0 <= prices[i] <= 1000
"""

from typing import List


class Solution:
    # ── State Machine DP O(n·k) time, O(k) space ──────────────────────────
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)
        if n < 2 or k == 0:
            return 0

        # If k >= n/2, it's equivalent to unlimited transactions
        if k >= n // 2:
            profit = 0
            for i in range(1, n):
                if prices[i] > prices[i - 1]:
                    profit += prices[i] - prices[i - 1]
            return profit

        # buy[t] = max profit after t-th buy
        # sell[t] = max profit after t-th sell
        buy = [float('-inf')] * (k + 1)
        sell = [0] * (k + 1)

        for price in prices:
            for t in range(1, k + 1):
                buy[t] = max(buy[t], sell[t - 1] - price)
                sell[t] = max(sell[t], buy[t] + price)

        return sell[k]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        (2, [2, 4, 1], 2),
        (2, [3, 2, 6, 5, 0, 3], 7),
        (1, [1, 2], 1),
        (2, [1], 0),
        (3, [3, 3, 5, 0, 0, 3, 1, 4], 8),
    ]

    for k, prices, expected in tests:
        result = sol.maxProfit(k, prices)
        status = "✓" if result == expected else "✗"
        print(f"k={k}, {prices} → {result} (expected {expected}) {status}")
