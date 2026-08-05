"""
LeetCode 322: Coin Change

You are given an integer array coins representing coins of different
denominations and an integer amount representing a total amount of
money. Return the fewest number of coins that you need to make up
that amount. If that amount of money cannot be made up by any
combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Constraints:
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 2^31 - 1
- 0 <= amount <= 10^4
"""

from typing import List


class Solution:
    # ── Unbounded Knapsack DP O(amount · len(coins)) time, O(amount) space
    def coinChange(self, coins: List[int], amount: int) -> int:
        """dp[a] = min coins to make amount a."""
        INF = amount + 1
        dp = [INF] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for a in range(coin, amount + 1):
                dp[a] = min(dp[a], dp[a - coin] + 1)

        return dp[amount] if dp[amount] != INF else -1

    # ── BFS approach O(amount · len(coins)) worst case ───────────────────
    def coinChange_bfs(self, coins: List[int], amount: int) -> int:
        """BFS: shortest path from 0 to amount."""
        from collections import deque

        if amount == 0:
            return 0

        coins.sort(reverse=True)
        queue = deque([(0, 0)])  # (current_sum, steps)
        visited = {0}

        while queue:
            cur, steps = queue.popleft()
            for coin in coins:
                nxt = cur + coin
                if nxt == amount:
                    return steps + 1
                if nxt < amount and nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, steps + 1))

        return -1


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 2, 5], 11, 3),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1, 2, 5], 100, 20),
        ([186, 419, 83, 408], 6249, 20),
    ]

    for coins, amount, expected in tests:
        r1 = sol.coinChange(coins, amount)
        ok = r1 == expected
        print(f"coins={coins}, amount={amount} → {r1} (expected {expected}) {'✓' if ok else '✗'}")
