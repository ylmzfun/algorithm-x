"""
LeetCode #283: Move Zeroes
https://leetcode.com/problems/move-zeroes/

Given an integer array `nums`, move all 0's to the end of it while maintaining the
relative order of the non-zero elements. Note that you must do this in-place without
making a copy of the array.

Constraints:
- 1 <= nums.length <= 10^4
- -2^31 <= nums[i] <= 2^31 - 1

Approach: Two Pointers (Snowball or Swap)
    Maintain a `nonzero` pointer tracking where the next non-zero element should go.
    Iterate with `current` pointer; whenever a non-zero is found, swap it with the
    element at `nonzero` and advance `nonzero`.
    O(n) time, O(1) space.
"""

from typing import List


def move_zeroes(nums: List[int]) -> None:
    """Two-pointer in-place: O(n) time, O(1) space."""
    nonzero = 0  # Position to place the next non-zero

    for current in range(len(nums)):
        if nums[current] != 0:
            nums[nonzero], nums[current] = nums[current], nums[nonzero]
            nonzero += 1


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([1, 2, 3], [1, 2, 3]),
        ([0, 0, 1], [1, 0, 0]),
        ([4, 2, 4, 0, 0, 3, 0, 5, 1, 0], [4, 2, 4, 3, 5, 1, 0, 0, 0, 0]),
    ]

    all_pass = True
    for nums, expected in test_cases:
        nums_copy = nums[:]
        move_zeroes(nums_copy)
        pass_flag = nums_copy == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => {nums_copy} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
