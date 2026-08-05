"""
LeetCode 122: Best Time to Buy and Sell Stock II

You are given an integer array prices where prices[i] is the price of
a given stock on the i-th day. On each day, you may decide to buy
and/or sell the stock. You can only hold at most one share of the
stock at any time. However, you can buy it then immediately sell it
on the same day.

Find and return the maximum profit you can achieve.

Constraints:
- 1 <= prices.length <= 3 * 10^4
- 0 <= prices[i] <= 10^4
"""

from typing import List


class Solution:
    # ── Greedy: sum all positive differences O(n) time, O(1) space ────────
    def maxProfit(self, prices: List[int]) -> int:
        """Sum all positive day-to-day price increases."""
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]
        return profit

    # ── DP State Machine O(n) time, O(1) space ────────────────────────────
    def maxProfit_dp(self, prices: List[int]) -> int:
        """
        hold = max profit ending with stock held
        cash = max profit ending with no stock held
        """
        hold, cash = float('-inf'), 0
        for price in prices:
            prev_cash = cash
            cash = max(cash, hold + price)
            hold = max(hold, prev_cash - price)
        return cash


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([7, 1, 5, 3, 6, 4], 7),
        ([1, 2, 3, 4, 5], 4),
        ([7, 6, 4, 3, 1], 0),
        ([1, 5, 3, 8], 9),
    ]

    for prices, expected in tests:
        r1 = sol.maxProfit(prices)
        r2 = sol.maxProfit_dp(prices)
        ok = r1 == r2 == expected
        print(f"{prices} → Greedy={r1}, DP={r2} | {'✓' if ok else '✗'}")
