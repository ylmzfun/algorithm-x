"""
90. Subsets II
https://leetcode.com/problems/subsets-ii/

Given an integer array nums that may contain duplicates, return all possible
subsets (the power set). The solution set must not contain duplicate subsets.
Return the answer in any order.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with sorting and duplicate skip
# Sort first. For each position, skip same-valued elements at the same
# recursion level to avoid duplicate subsets.
# Time: O(N × 2^N) worst
# Space: O(N) recursion depth
# ──────────────────────────────────────────────────────────────────────────────
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    """Backtracking: skip duplicates at same level after sorting."""
    nums.sort()
    result: list[list[int]] = []

    def backtrack(start: int, current: list[int]) -> None:
        result.append(current[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, nums: list[int], expected: list[list[int]]):
        result = subsets_with_dup(nums)
        result_set = {tuple(s) for s in result}
        expected_set = {tuple(s) for s in expected}
        ok = result_set == expected_set and len(result) == len(expected)
        print(f"[{label}] {'✓' if ok else '✗'} (got {len(result)} subsets)")

    test("Example 1", [1, 2, 2],
         [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])
    test("Example 2", [0], [[], [0]])
    test("All same", [1, 1], [[], [1], [1, 1]])
    print("\nAll subsets II tests completed.")
