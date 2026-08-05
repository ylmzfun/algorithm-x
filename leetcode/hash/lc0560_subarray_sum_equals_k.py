"""
560. Subarray Sum Equals K
https://leetcode.com/problems/subarray-sum-equals-k/

Given an array of integers nums and an integer k, return the total number of
subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.
"""

from __future__ import annotations
from collections import defaultdict


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Prefix Sum + Hash Map
# If prefix[j] - prefix[i-1] == k, then subarray nums[i..j] sums to k.
# So at position j, count how many prefix[i-1] == prefix[j] - k existed.
# Time: O(N)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def subarray_sum(nums: list[int], k: int) -> int:
    """Prefix sum with hash map tracking cumulative sum frequencies."""
    prefix_count: dict[int, int] = defaultdict(int)
    prefix_count[0] = 1  # empty prefix before start
    cur_sum = 0
    count = 0

    for num in nums:
        cur_sum += num
        count += prefix_count.get(cur_sum - k, 0)
        prefix_count[cur_sum] += 1

    return count


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, nums: list[int], k: int, expected: int):
        result = subarray_sum(nums, k)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [1, 1, 1], 2, 2)  # [1,1] and [1,1]
    test("Example 2", [1, 2, 3], 3, 2)  # [1,2], [3]
    test("Example 3", [1, -1, 0], 0, 3)  # [1,-1], [0], [1,-1,0]
    test("Negative numbers", [-1, -1, 1], 0, 1)
    print("\nAll subarray sum equals k tests completed.")
