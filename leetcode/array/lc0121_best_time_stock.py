"""
LeetCode #121: Best Time to Buy and Sell Stock
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

You are given an array `prices` where prices[i] is the price of a given stock on the
i-th day. You want to maximize your profit by choosing a single day to buy one stock
and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve
any profit, return 0.

Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4

Approach: One-pass (Kadane-like)
    Track the minimum price seen so far. At each step, calculate potential profit
    (current price - min price) and update max profit.
    O(n) time, O(1) space.
"""

from typing import List


def max_profit(prices: List[int]) -> int:
    """One-pass: track min price and max profit. O(n) time, O(1) space."""
    min_price = float('inf')
    max_prof = 0

    for price in prices:
        if price < min_price:
            min_price = price
        else:
            prof = price - min_price
            if prof > max_prof:
                max_prof = prof

    return max_prof


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([7, 1, 5, 3, 6, 4], 5),
        ([7, 6, 4, 3, 1], 0),
        ([1, 2], 1),
        ([2, 1, 2, 1, 0, 1, 2], 2),
        ([3, 3, 3, 3], 0),
    ]

    all_pass = True
    for prices, expected in test_cases:
        result = max_profit(prices)
        pass_flag = result == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | prices={prices} => {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
