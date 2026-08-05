"""
LeetCode 121: Best Time to Buy and Sell Stock

You are given an array prices where prices[i] is the price of a given
stock on the i-th day. You want to maximize your profit by choosing a
single day to buy one stock and choosing a different day in the future
to sell that stock.

Return the maximum profit you can achieve from this transaction.
If you cannot achieve any profit, return 0.

Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4
"""

from typing import List


class Solution:
    # ── Kadane Variant (Max Subarray Difference) O(n) time, O(1) space ────
    def maxProfit(self, prices: List[int]) -> int:
        """
        Track the minimum price seen so far.
        At each day, compute profit if sold today.
        Equivalent to Kadane on daily price differences.
        """
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            if price < min_price:
                min_price = price
            else:
                max_profit = max(max_profit, price - min_price)

        return max_profit

    # ── Kadane on differences ─────────────────────────────────────────────
    def maxProfit_diff(self, prices: List[int]) -> int:
        """Max subarray sum on daily price changes."""
        max_ending_here = max_so_far = 0
        for i in range(1, len(prices)):
            diff = prices[i] - prices[i - 1]
            max_ending_here = max(0, max_ending_here + diff)
            max_so_far = max(max_so_far, max_ending_here)
        return max_so_far


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([7, 1, 5, 3, 6, 4], 5),
        ([7, 6, 4, 3, 1], 0),
        ([1, 2, 3, 4, 5], 4),
        ([2, 1, 4], 3),
    ]

    for prices, expected in tests:
        r1 = sol.maxProfit(prices)
        r2 = sol.maxProfit_diff(prices)
        ok = r1 == r2 == expected
        print(f"{prices} → MinTrack={r1}, KadaneDiff={r2} | {'✓' if ok else '✗'}")
