"""
LeetCode #152: Maximum Product Subarray
https://leetcode.com/problems/maximum-product-subarray/

Given an integer array `nums`, find a contiguous non-empty subarray within the array
that has the largest product, and return the product.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any subarray of nums will fit in a 32-bit integer.

Approach: Kadane Variant (Track Min and Max)
    Because a negative * negative = positive, we need to track both the max and
    min product ending at each position. At each step, update:
    - current_max = max(num, num * prev_max, num * prev_min)
    - current_min = min(num, num * prev_max, num * prev_min)
    O(n) time, O(1) space.
"""

from typing import List


def max_product(nums: List[int]) -> int:
    """Kadane variant tracking min and max: O(n) time, O(1) space."""
    if not nums:
        return 0

    global_max = nums[0]
    cur_max = nums[0]
    cur_min = nums[0]

    for num in nums[1:]:
        # Temporarily store cur_max because it will be overwritten
        candidates = (num, num * cur_max, num * cur_min)
        cur_max = max(candidates)
        cur_min = min(candidates)
        global_max = max(global_max, cur_max)

    return global_max


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([2, 3, -2, 4], 6),
        ([-2, 0, -1], 0),
        ([-2, 3, -4], 24),
        ([0, 2], 2),
        ([-2], -2),
        ([3, -1, 4], 4),
    ]

    all_pass = True
    for nums, expected in test_cases:
        result = max_product(nums)
        pass_flag = result == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
