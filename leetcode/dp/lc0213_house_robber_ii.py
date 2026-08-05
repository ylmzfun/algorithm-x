"""
LeetCode 213: House Robber II

You are a professional robber planning to rob houses along a street.
Each house has a certain amount of money stashed. All houses at this
place are arranged in a circle. That means the first house is the
neighbor of the last one. Adjacent houses have a security system
connected.

Given an integer array nums representing the amount of money of each
house, return the maximum amount of money you can rob tonight without
alerting the police.

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000
"""

from typing import List


class Solution:
    # ── Two Passes: rob [0..n-2] or [1..n-1] O(n) time, O(1) space ────────
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[0], nums[1])

        def rob_linear(arr: List[int]) -> int:
            prev2 = arr[0]
            prev1 = max(arr[0], arr[1])
            for i in range(2, len(arr)):
                curr = max(prev1, prev2 + arr[i])
                prev2, prev1 = prev1, curr
            return prev1

        # Case 1: exclude last house
        # Case 2: exclude first house
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([2, 3, 2], 3),
        ([1, 2, 3, 1], 4),
        ([1, 2, 3], 3),
        ([1], 1),
        ([2, 7, 9, 3, 1], 11),
        ([1, 1, 1, 1], 2),
    ]

    for nums, expected in tests:
        result = sol.rob(nums)
        status = "✓" if result == expected else "✗"
        print(f"{nums} → {result} (expected {expected}) {status}")
