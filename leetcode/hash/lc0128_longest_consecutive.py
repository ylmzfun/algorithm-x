"""
128. Longest Consecutive Sequence
https://leetcode.com/problems/longest-consecutive-sequence/

Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: HashSet + Greedy streak building
# Insert all numbers into a set. For each number that is the start of a
# sequence (num-1 not in set), count consecutive numbers upward.
# Time: O(N) — each element is processed at most twice.
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def longest_consecutive(nums: list[int]) -> int:
    """Find longest streak by checking from sequence starts only."""
    num_set = set(nums)
    max_len = 0

    for num in num_set:
        # Only start counting if num is the beginning of a sequence
        if num - 1 not in num_set:
            cur = num
            cur_len = 1
            while cur + 1 in num_set:
                cur += 1
                cur_len += 1
            max_len = max(max_len, cur_len)

    return max_len


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, nums: list[int], expected: int):
        result = longest_consecutive(nums)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [100, 4, 200, 1, 3, 2], 4)  # 1,2,3,4
    test("Example 2", [0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9)  # 0..8
    test("Empty", [], 0)
    test("Duplicates", [1, 2, 2, 3], 3)
    print("\nAll longest consecutive sequence tests completed.")
