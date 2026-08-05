"""
LeetCode #169: Majority Element
https://leetcode.com/problems/majority-element/

Given an array `nums` of size n, return the majority element. The majority element is
the element that appears more than ⌊n / 2⌋ times. You may assume that the majority
element always exists in the array.

Constraints:
- n == nums.length
- 1 <= n <= 5 * 10^4
- -10^9 <= nums[i] <= 10^9

Approach 1: Boyer-Moore Voting Algorithm
    Maintain a candidate and a count. When count == 0, pick current element as new
    candidate. Increment count when matching, decrement when different.
    The majority element survives cancellations. O(n) time, O(1) space.

Approach 2: Hash Map
    Count frequencies and return the element with count > n/2. O(n) time, O(n) space.

Approach 3: Sorting
    Sort and return the middle element. O(n log n) time, O(1) space.
"""

from typing import List
from collections import Counter


def majority_element_boyer_moore(nums: List[int]) -> int:
    """Boyer-Moore voting: O(n) time, O(1) space."""
    candidate = 0
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1

    return candidate


def majority_element_hash(nums: List[int]) -> int:
    """Hash map counting: O(n) time, O(n) space."""
    counts = Counter(nums)
    n = len(nums)
    for num, cnt in counts.items():
        if cnt > n // 2:
            return num
    return -1  # Should not reach given constraints


# ── Default export ──
majorityElement = majority_element_boyer_moore


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([3, 2, 3], 3),
        ([2, 2, 1, 1, 1, 2, 2], 2),
        ([1], 1),
        ([6, 5, 5], 5),
        ([-1, -1, -1, 2, 2], -1),
    ]

    all_pass = True
    for nums, expected in test_cases:
        r1 = majority_element_boyer_moore(nums)
        r2 = majority_element_hash(nums)
        pass_flag = r1 == expected and r2 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => bm={r1}, hash={r2} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
