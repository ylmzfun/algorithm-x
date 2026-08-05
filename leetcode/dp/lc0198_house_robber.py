"""
LeetCode 198: House Robber

You are a professional robber planning to rob houses along a street.
Each house has a certain amount of money stashed. All houses at this
place are arranged in a line. Adjacent houses have security systems
connected and it will automatically contact the police if two adjacent
houses were broken into on the same night.

Given an integer array nums representing the amount of money of each
house, return the maximum amount of money you can rob tonight without
alerting the police.

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 400
"""

from typing import List


class Solution:
    # ── Classic 1D DP O(n) time, O(1) space ───────────────────────────────
    def rob(self, nums: List[int]) -> int:
        """
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
        Optimized to two variables.
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        prev2 = nums[0]                     # dp[i-2]
        prev1 = max(nums[0], nums[1])       # dp[i-1]

        for i in range(2, len(nums)):
            curr = max(prev1, prev2 + nums[i])
            prev2, prev1 = prev1, curr

        return prev1


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 2, 3, 1], 4),
        ([2, 7, 9, 3, 1], 12),
        ([2, 1, 1, 2], 4),
        ([1], 1),
        ([0], 0),
    ]

    for nums, expected in tests:
        result = sol.rob(nums)
        status = "✓" if result == expected else "✗"
        print(f"{nums} → {result} (expected {expected}) {status}")
