"""
LeetCode 53: Maximum Subarray

Given an integer array nums, find the subarray with the largest sum,
and return its sum.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
"""

from typing import List


class Solution:
    # ── Kadane's Algorithm O(n) time, O(1) space ───────────────────────────
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Kadane's algorithm:
        At each position i, decide whether to extend the previous subarray
        or start fresh. dp[i] = max(nums[i], dp[i-1] + nums[i]).
        Optimized to O(1) space by tracking only the previous value.
        """
        max_ending_here = max_so_far = nums[0]

        for x in nums[1:]:
            max_ending_here = max(x, max_ending_here + x)
            max_so_far = max(max_so_far, max_ending_here)

        return max_so_far

    # ── Divide & Conquer O(n log n) time ───────────────────────────────────
    def maxSubArray_divide_conquer(self, nums: List[int]) -> int:
        """Divide and conquer approach for comparison."""
        def helper(left: int, right: int) -> int:
            if left == right:
                return nums[left]

            mid = (left + right) // 2
            left_max = helper(left, mid)
            right_max = helper(mid + 1, right)

            # Cross sum
            l_sum = float('-inf')
            cur = 0
            for i in range(mid, left - 1, -1):
                cur += nums[i]
                l_sum = max(l_sum, cur)

            r_sum = float('-inf')
            cur = 0
            for i in range(mid + 1, right + 1):
                cur += nums[i]
                r_sum = max(r_sum, cur)

            return max(left_max, right_max, l_sum + r_sum)

        return helper(0, len(nums) - 1)


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-1], -1),
        ([-2, -1], -1),
        ([1, 2, 3, 4], 10),
    ]

    for nums, expected in tests:
        r1 = sol.maxSubArray(nums)
        r2 = sol.maxSubArray_divide_conquer(nums)
        ok = r1 == r2 == expected
        print(f"{nums} → Kadane={r1}, D&C={r2} | {'✓' if ok else '✗'}")
