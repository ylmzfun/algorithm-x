"""
LeetCode 309: Best Time to Buy and Sell Stock with Cooldown

You are given an array prices where prices[i] is the price of a given
stock on the i-th day. Find the maximum profit you can achieve.
You may complete as many transactions as you like (i.e., buy one and
sell one share of the stock multiple times) with the following
restrictions:
- After you sell your stock, you cannot buy stock on the next day
  (i.e., cooldown one day).

Note: You may not engage in multiple transactions simultaneously
(i.e., you must sell the stock before you buy again).

Constraints:
- 1 <= prices.length <= 5000
- 0 <= prices[i] <= 1000
"""

from typing import List


class Solution:
    # ── State Machine DP O(n) time, O(1) space ────────────────────────────
    def maxProfit(self, prices: List[int]) -> int:
        """
        Three states:
        - hold: max profit ending with stock held
        - sold: max profit ending with stock just sold (in cooldown)
        - rest: max profit ending with no stock and not in cooldown
        """
        hold: int = float('-inf')
        sold: int = 0
        rest: int = 0

        for price in prices:
            prev_sold = sold
            hold = max(hold, rest - price)
            sold = hold + price
            rest = max(rest, prev_sold)

        return max(sold, rest)


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 2, 3, 0, 2], 3),
        ([1], 0),
        ([1, 2, 4], 3),
        ([2, 1, 4], 3),
        ([6, 1, 3, 2, 4, 7], 6),
    ]

    for prices, expected in tests:
        result = sol.maxProfit(prices)
        status = "✓" if result == expected else "✗"
        print(f"{prices} → {result} (expected {expected}) {status}")
