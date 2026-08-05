"""
LeetCode 152: Maximum Product Subarray

Given an integer array nums, find a subarray that has the largest
product, and return the product.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any subarray of nums is guaranteed to fit in a
  32-bit integer.
"""

from typing import List


class Solution:
    # ── Single-Pass DP O(n) time, O(1) space ──────────────────────────────
    def maxProduct(self, nums: List[int]) -> int:
        """
        Track both max and min product ending at each position,
        because a negative number can flip min to max.
        """
        max_ending = min_ending = result = nums[0]

        for x in nums[1:]:
            candidates = (x, max_ending * x, min_ending * x)
            max_ending = max(candidates)
            min_ending = min(candidates)
            result = max(result, max_ending)

        return result

    # ── Two-Pass (Prefix/Suffix) O(n) time, O(1) space ────────────────────
    def maxProduct_twopass(self, nums: List[int]) -> int:
        """Compute prefix and suffix products, reset on zero."""
        n = len(nums)
        result = float('-inf')
        prefix = suffix = 1

        for i in range(n):
            prefix *= nums[i]
            suffix *= nums[n - 1 - i]
            result = max(result, prefix, suffix)
            if prefix == 0:
                prefix = 1
            if suffix == 0:
                suffix = 1

        return result


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([2, 3, -2, 4], 6),
        ([-2, 0, -1], 0),
        ([-2, 3, -4], 24),
        ([0, 2], 2),
        ([3, -1, 4], 4),
        ([-1, -2, -3, -4], 24),
    ]

    for nums, expected in tests:
        r1 = sol.maxProduct(nums)
        r2 = sol.maxProduct_twopass(nums)
        ok = r1 == r2 == expected
        print(f"{nums} → SinglePass={r1}, TwoPass={r2} | {'✓' if ok else '✗'}")
