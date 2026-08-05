"""
LeetCode #53: Maximum Subarray
https://leetcode.com/problems/maximum-subarray/

Given an integer array `nums`, find the subarray with the largest sum, and return
its sum.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Approach 1: Kadane's Algorithm
    Maintain current_sum as the max subarray sum ending at the current position.
    At each step: current_sum = max(num, current_sum + num).
    Track global maximum. O(n) time, O(1) space.

Approach 2: Divide and Conquer
    Split array, find max crossing subarray, and combine. O(n log n) time.
"""

from typing import List


def max_subarray_kadane(nums: List[int]) -> int:
    """Kadane's algorithm: O(n) time, O(1) space."""
    current_sum = nums[0]
    max_sum = nums[0]

    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum


def max_subarray_dc(nums: List[int]) -> int:
    """Divide and conquer: O(n log n) time."""

    def helper(left: int, right: int) -> int:
        if left == right:
            return nums[left]

        mid = (left + right) // 2
        left_max = helper(left, mid)
        right_max = helper(mid + 1, right)

        # Crossing sum
        cross_left = float('-inf')
        s = 0
        for i in range(mid, left - 1, -1):
            s += nums[i]
            cross_left = max(cross_left, s)

        cross_right = float('-inf')
        s = 0
        for i in range(mid + 1, right + 1):
            s += nums[i]
            cross_right = max(cross_right, s)

        return max(left_max, right_max, cross_left + cross_right)

    return helper(0, len(nums) - 1)


# ── Default export ──
maxSubArray = max_subarray_kadane


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-1], -1),
        ([-2, -3, -1], -1),
    ]

    all_pass = True
    for nums, expected in test_cases:
        r1 = max_subarray_kadane(nums)
        r2 = max_subarray_dc(nums)
        pass_flag = r1 == expected and r2 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => kadane={r1}, dc={r2} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
