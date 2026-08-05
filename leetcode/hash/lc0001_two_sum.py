"""
1. Two Sum
https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, return indices of the
two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may
not use the same element twice. You can return the answer in any order.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Hash Map (one pass)
# For each num, check if (target - num) has been seen before.
# Time: O(N)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def two_sum(nums: list[int], target: int) -> list[int]:
    """One-pass hash map: check complement while iterating."""
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []  # unreachable given problem guarantee


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: Two-pointer (requires sorted copy with index tracking)
# Time: O(N log N)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def two_sum_two_pointer(nums: list[int], target: int) -> list[int]:
    """Two-pointer on sorted (value, index) pairs."""
    indexed = sorted((num, i) for i, num in enumerate(nums))
    left, right = 0, len(indexed) - 1
    while left < right:
        cur = indexed[left][0] + indexed[right][0]
        if cur == target:
            return [indexed[left][1], indexed[right][1]]
        elif cur < target:
            left += 1
        else:
            right -= 1
    return []  # unreachable


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, nums: list[int], target: int, expected: list[int]):
        methods = [
            ("Hash", two_sum),
            ("Two-pointer", two_sum_two_pointer),
        ]
        for name, fn in methods:
            result = fn(nums, target)
            ok = sorted(result) == sorted(expected)
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [2, 7, 11, 15], 9, [0, 1])
    test("Example 2", [3, 2, 4], 6, [1, 2])
    test("Example 3", [3, 3], 6, [0, 1])
    print("\nAll two sum tests completed.")
