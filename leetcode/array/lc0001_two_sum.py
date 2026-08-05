"""
LeetCode #1: Two Sum
https://leetcode.com/problems/two-sum/

Given an array of integers `nums` and an integer `target`, return indices of the two
numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use
the same element twice. You can return the answer in any order.

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.

Approach 1: Brute Force
    Nested loop checking every pair. O(n^2) time, O(1) space.

Approach 2: Hash Map (One-pass)
    Iterate once; for each element, check if `target - num` is in the hash map.
    If found, return indices; otherwise store the current element → index.
    O(n) time, O(n) space.
"""

from typing import List


def two_sum_brute(nums: List[int], target: int) -> List[int]:
    """Brute force: check all pairs O(n^2)."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []  # Should not reach due to problem constraints


def two_sum_hash(nums: List[int], target: int) -> List[int]:
    """One-pass hash map lookup O(n)."""
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


# ── Default export ──
twoSum = two_sum_hash


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
        ([1, 5, 3, 8, 2], 10, [3, 4]),  # 8 + 2 = 10
        ([0, 4, 3, 0], 0, [0, 3]),
    ]

    all_pass = True
    for nums, target, expected in test_cases:
        result = two_sum_hash(nums, target)
        pass_flag = sorted(result) == sorted(expected)
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums}, target={target} => {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
