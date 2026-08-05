"""
LeetCode #34: Find First and Last Position of Element in Sorted Array
https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

Given an array of integers `nums` sorted in non-decreasing order, find the starting
and ending position of a given `target` value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- nums is a non-decreasing array.
- -10^9 <= target <= 10^9

Approach: Two Binary Searches
    Use a modified binary search to find the first occurrence (leftmost) and
    last occurrence (rightmost) of target. Each search is O(log n).
    Total: O(log n) time, O(1) space.
"""

from typing import List


def _find_bound(nums: List[int], target: int, find_first: bool) -> int:
    """Find the first (find_first=True) or last (find_first=False) index of target."""
    left, right = 0, len(nums) - 1
    bound = -1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            bound = mid
            if find_first:
                right = mid - 1  # Continue searching left
            else:
                left = mid + 1   # Continue searching right
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return bound


def search_range(nums: List[int], target: int) -> List[int]:
    """Find the first and last position of target. O(log n) time, O(1) space."""
    if not nums:
        return [-1, -1]

    first = _find_bound(nums, target, find_first=True)
    if first == -1:
        return [-1, -1]

    last = _find_bound(nums, target, find_first=False)
    return [first, last]


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([5, 7, 7, 8, 8, 10], 8, [3, 4]),
        ([5, 7, 7, 8, 8, 10], 6, [-1, -1]),
        ([], 0, [-1, -1]),
        ([1], 1, [0, 0]),
        ([2, 2, 2, 2, 2], 2, [0, 4]),
        ([1, 2, 3, 4, 5], 5, [4, 4]),
    ]

    all_pass = True
    for nums, target, expected in test_cases:
        result = search_range(nums, target)
        pass_flag = result == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums}, target={target} => {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
