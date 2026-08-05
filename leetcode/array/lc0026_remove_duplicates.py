"""
LeetCode #26: Remove Duplicates from Sorted Array
https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Given an integer array `nums` sorted in non-decreasing order, remove the duplicates
in-place such that each unique element appears only once. The relative order of the
elements should be kept the same. Then return the number of unique elements in nums.

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100
- nums is sorted in non-decreasing order.

Approach: Two Pointers (Fast-Slow)
    slow pointer tracks the position for the next unique element.
    fast pointer scans through the array.
    When a new unique element is found, place it at the slow pointer and advance slow.
    O(n) time, O(1) space.
"""

from typing import List


def remove_duplicates(nums: List[int]) -> int:
    """In-place removal of duplicates; returns count of unique elements.
    O(n) time, O(1) space."""
    if not nums:
        return 0

    slow = 0  # Index for placing the next unique element

    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    return slow + 1  # Length of the unique portion


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 1, 2], 2, [1, 2]),
        ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 5, [0, 1, 2, 3, 4]),
        ([1], 1, [1]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([1, 1, 1, 1], 1, [1]),
    ]

    all_pass = True
    for nums, expected_k, expected_prefix in test_cases:
        nums_copy = nums[:]
        k = remove_duplicates(nums_copy)
        pass_flag = k == expected_k and nums_copy[:k] == expected_prefix
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => k={k}, first_k={nums_copy[:k]} "
              f"(expected k={expected_k}, {expected_prefix})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
