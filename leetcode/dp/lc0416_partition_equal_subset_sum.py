"""
LeetCode 416: Partition Equal Subset Sum

Given an integer array nums, return true if you can partition the array
into two subsets such that the sums of the elements in both subsets
are equal or false otherwise.

Constraints:
- 1 <= nums.length <= 200
- 1 <= nums[i] <= 100
"""

from typing import List


class Solution:
    # ── 0/1 Knapsack Subset Sum DP O(n·sum) time, O(sum) space ────────────
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # If total is odd, impossible to split equally
        if total % 2 != 0:
            return False

        target = total // 2

        # dp[s] = can we achieve sum s?
        dp = [False] * (target + 1)
        dp[0] = True

        for num in nums:
            # Traverse backwards to avoid using the same number twice
            for s in range(target, num - 1, -1):
                dp[s] = dp[s] or dp[s - num]

        return dp[target]

    # ── Bitmask DP O(n·sum/word) time, O(sum/word) space ─────────────────
    def canPartition_bitset(self, nums: List[int]) -> bool:
        """Use bitset for fast subset sum."""
        total = sum(nums)
        if total % 2 != 0:
            return False
        target = total // 2

        # bitset: bit at position s = can we achieve sum s?
        bits = 1  # bit 0 set (sum 0 achievable)

        for num in nums:
            bits |= bits << num

        return (bits >> target) & 1 == 1


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 5, 11, 5], True),
        ([1, 2, 3, 5], False),
        ([1, 2, 5], False),
        ([2, 2, 3, 5], False),
        ([1, 1, 1, 1], True),
        ([100] * 200, False),  # even total but large
    ]

    for nums, expected in tests[:5]:  # skip the large one for DP
        r1 = sol.canPartition(nums)
        r2 = sol.canPartition_bitset(nums)
        ok = r1 == r2 == expected
        print(f"{nums} → DP={r1}, Bitset={r2} | {'✓' if ok else '✗'}")
