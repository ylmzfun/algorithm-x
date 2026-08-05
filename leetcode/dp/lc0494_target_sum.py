"""
LeetCode 494: Target Sum

You are given an integer array nums and an integer target.

You want to build an expression out of nums by adding one of the
symbols '+' and '-' before each integer in nums and then concatenate
all the integers. Return the number of different expressions that
you can build, which evaluates to target.

Constraints:
- 1 <= nums.length <= 20
- 0 <= nums[i] <= 1000
- 0 <= sum(nums[i]) <= 1000
- -1000 <= target <= 1000
"""

from typing import List


class Solution:
    # ── Subset Sum DP O(n·sum) time, O(sum) space ─────────────────────────
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        """
        Let P = subset with +, N = subset with -.
        sum(P) - sum(N) = target
        sum(P) + sum(N) = total
        => 2 * sum(P) = target + total
        => sum(P) = (target + total) / 2
        So we count subsets that sum to (target + total) / 2.
        """
        total = sum(nums)

        # sum(P) must be non-negative integer
        if (target + total) % 2 != 0 or target + total < 0:
            return 0

        subset_target = (target + total) // 2
        if subset_target > total:
            return 0

        # Count subsets summing to subset_target (0/1 knapsack)
        dp = [0] * (subset_target + 1)
        dp[0] = 1

        for num in nums:
            for s in range(subset_target, num - 1, -1):
                dp[s] += dp[s - num]

        return dp[subset_target]

    # ── DFS with Memoization ──────────────────────────────────────────────
    def findTargetSumWays_dfs(self, nums: List[int], target: int) -> int:
        from functools import lru_cache

        @lru_cache(None)
        def dfs(i: int, cur: int) -> int:
            if i == len(nums):
                return 1 if cur == target else 0
            return dfs(i + 1, cur + nums[i]) + dfs(i + 1, cur - nums[i])

        return dfs(0, 0)


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 1, 1, 1, 1], 3, 5),
        ([1], 1, 1),
        ([1], 2, 0),
        ([0, 0, 0, 0, 0], 0, 32),
        ([1, 2, 1], 0, 2),
    ]

    for nums, target, expected in tests:
        r1 = sol.findTargetSumWays(nums, target)
        r2 = sol.findTargetSumWays_dfs(nums, target) if len(nums) <= 15 else r1
        ok = r1 == expected
        print(f"{nums}, target={target} → DP={r1} | {'✓' if ok else '✗'}")
