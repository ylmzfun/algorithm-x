"""
LeetCode 300: Longest Increasing Subsequence

Given an integer array nums, return the length of the longest strictly
increasing subsequence.

Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4
"""

from typing import List
import bisect


class Solution:
    # ── DP O(n²) time, O(n) space ────────────────────────────────────────
    def lengthOfLIS_dp(self, nums: List[int]) -> int:
        """dp[i] = length of LIS ending at index i."""
        n = len(nums)
        dp = [1] * n

        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

    # ── Patience Sorting O(n log n) time, O(n) space ─────────────────────
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Maintain tails array where tails[i] = smallest tail of all
        increasing subsequences of length i+1.
        Use binary search to update tails.
        """
        tails: List[int] = []

        for x in nums:
            idx = bisect.bisect_left(tails, x)
            if idx == len(tails):
                tails.append(x)
            else:
                tails[idx] = x

        return len(tails)

    # ── Reconstruct LIS ──────────────────────────────────────────────────
    def reconstructLIS(self, nums: List[int]) -> List[int]:
        """Return one LIS using patience sorting."""
        n = len(nums)
        if n == 0:
            return []

        tails: List[int] = []
        tail_indices: List[int] = []
        prev = [-1] * n

        for i, x in enumerate(nums):
            idx = bisect.bisect_left(tails, x)
            if idx == len(tails):
                tails.append(x)
                tail_indices.append(i)
            else:
                tails[idx] = x
                tail_indices[idx] = i
            if idx > 0:
                prev[i] = tail_indices[idx - 1]

        # Reconstruct
        result = []
        cur = tail_indices[-1]
        while cur != -1:
            result.append(nums[cur])
            cur = prev[cur]
        return result[::-1]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),
        ([0, 1, 0, 3, 2, 3], 4),
        ([7, 7, 7, 7, 7], 1),
        ([1, 3, 6, 7, 9, 4, 10, 5, 6], 6),
    ]

    for nums, expected in tests:
        r1 = sol.lengthOfLIS_dp(nums)
        r2 = sol.lengthOfLIS(nums)
        ok = r1 == r2 == expected
        seq = sol.reconstructLIS(nums)
        print(f"{nums} → DP={r1}, Patience={r2} | {'✓' if ok else '✗'}")
        if ok:
            print(f"  LIS: {seq}")
