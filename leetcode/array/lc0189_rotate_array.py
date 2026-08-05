"""
LeetCode #189: Rotate Array
https://leetcode.com/problems/rotate-array/

Given an integer array `nums`, rotate the array to the right by `k` steps, where `k`
is non-negative. Do it in-place with O(1) extra space.

Constraints:
- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1
- 0 <= k <= 10^5

Approach 1: Reverse Method
    Step 1: Reverse the entire array.
    Step 2: Reverse the first k elements.
    Step 3: Reverse the remaining n - k elements.
    O(n) time, O(1) space.

Approach 2: Cyclic Replacements
    Move each element to its final position, following cycles.
    O(n) time, O(1) space.
"""

from typing import List


def _reverse(nums: List[int], left: int, right: int) -> None:
    """Reverse nums[left:right+1] in-place."""
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def rotate_reverse(nums: List[int], k: int) -> None:
    """Reverse method: O(n) time, O(1) space."""
    n = len(nums)
    k %= n  # Normalize k
    if k == 0:
        return

    _reverse(nums, 0, n - 1)
    _reverse(nums, 0, k - 1)
    _reverse(nums, k, n - 1)


# ── Default export ──
rotate = rotate_reverse


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]),
        ([-1, -100, 3, 99], 2, [3, 99, -1, -100]),
        ([1, 2], 3, [2, 1]),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1], 5, [1]),
    ]

    all_pass = True
    for nums, k, expected in test_cases:
        nums_copy = nums[:]
        rotate_reverse(nums_copy, k)
        pass_flag = nums_copy == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums}, k={k} => {nums_copy} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
