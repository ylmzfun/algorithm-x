"""
LeetCode #75: Sort Colors
https://leetcode.com/problems/sort-colors/

Given an array `nums` with n objects colored red (0), white (1), or blue (2), sort
them in-place so that objects of the same color are adjacent, with the colors in the
order red → white → blue.

You must solve this problem without using the library's sort function.

Constraints:
- n == nums.length
- 1 <= n <= 300
- nums[i] is either 0, 1, or 2.

Approach: Dutch National Flag (Three Pointers)
    Maintain three pointers: low (next 0 position), high (next 2 position),
    and current (scanning pointer).
    - When nums[current] == 0: swap with low, advance both.
    - When nums[current] == 2: swap with high, decrease high (don't advance current).
    - When nums[current] == 1: just advance current.
    O(n) time, O(1) space.
"""

from typing import List


def sort_colors(nums: List[int]) -> None:
    """Dutch National Flag: O(n) time, O(1) space."""
    low, current = 0, 0
    high = len(nums) - 1

    while current <= high:
        if nums[current] == 0:
            nums[low], nums[current] = nums[current], nums[low]
            low += 1
            current += 1
        elif nums[current] == 2:
            nums[high], nums[current] = nums[current], nums[high]
            high -= 1
            # Don't advance current — the swapped element needs inspection
        else:  # nums[current] == 1
            current += 1


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]),
        ([2, 0, 1], [0, 1, 2]),
        ([0], [0]),
        ([1, 2, 0], [0, 1, 2]),
        ([1, 1, 0, 0, 2, 2], [0, 0, 1, 1, 2, 2]),
    ]

    all_pass = True
    for nums, expected in test_cases:
        nums_copy = nums[:]
        sort_colors(nums_copy)
        pass_flag = nums_copy == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => {nums_copy} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
