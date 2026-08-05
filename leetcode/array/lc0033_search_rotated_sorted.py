"""
LeetCode #33: Search in Rotated Sorted Array
https://leetcode.com/problems/search-in-rotated-sorted-array/

There is an integer array `nums` sorted in ascending order (with distinct values).
Prior to being passed to your function, nums is possibly rotated at an unknown pivot
index k (1 <= k < nums.length) such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]].

Given the array `nums` after the possible rotation and an integer `target`, return the
index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique.
- nums is an ascending array that is possibly rotated.

Approach: Binary Search
    At each step, determine which half is properly sorted.
    Check if target lies within the sorted half; if so, search that half;
    otherwise, search the other half. O(log n) time, O(1) space.
"""

from typing import List


def search(nums: List[int], target: int) -> int:
    """Binary search in rotated sorted array. O(log n) time, O(1) space."""
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        # Check which half is sorted
        if nums[left] <= nums[mid]:  # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([1], 0, -1),
        ([1, 3], 3, 1),
        ([5, 1, 3], 5, 0),
        ([3, 1], 1, 1),
        ([4, 5, 6, 7, 0, 1, 2], 6, 2),
    ]

    all_pass = True
    for nums, target, expected in test_cases:
        result = search(nums, target)
        pass_flag = result == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums}, target={target} => {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
