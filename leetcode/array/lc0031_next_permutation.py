"""
LeetCode #31: Next Permutation
https://leetcode.com/problems/next-permutation/

A permutation of an array of integers is an arrangement of its members into a
sequence or linear order. The next permutation of an array of integers is the next
lexicographically greater permutation of its integers.

Given an array of integers `nums`, find the next permutation of nums. The replacement
must be in-place and use only constant extra memory.

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100

Approach: Single-pass (Narayana Pandita's algorithm)
    1. Find the first decreasing element from the right: nums[i] < nums[i+1].
    2. If such i exists, find the smallest element > nums[i] to the right (j).
       Swap nums[i] and nums[j].
    3. Reverse the subarray to the right of i (which is in descending order).
    O(n) time, O(1) space.
"""

from typing import List


def next_permutation(nums: List[int]) -> None:
    """Modify nums in-place to the next lexicographical permutation.
    O(n) time, O(1) space."""

    n = len(nums)
    # Step 1: Find first decreasing element from the right
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: Find the smallest element > nums[i] to the right
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # Swap
        nums[i], nums[j] = nums[j], nums[i]

    # Step 3: Reverse the suffix starting at i + 1
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3], [1, 3, 2]),
        ([3, 2, 1], [1, 2, 3]),
        ([1, 1, 5], [1, 5, 1]),
        ([1, 3, 2], [2, 1, 3]),
        ([2, 3, 1], [3, 1, 2]),
    ]

    all_pass = True
    for nums, expected in test_cases:
        nums_copy = nums[:]
        next_permutation(nums_copy)
        pass_flag = nums_copy == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => {nums_copy} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
