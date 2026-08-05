"""
78. Subsets
https://leetcode.com/problems/subsets/

Given an integer array nums of unique elements, return all possible
subsets (the power set). The solution set must not contain duplicate
subsets. Return the answer in any order.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Backtracking (cascading)
# For each element, include it or not. Build incrementally.
# Time: O(N × 2^N) — 2^N subsets, each up to size N.
# Space: O(N) recursion depth.
# ──────────────────────────────────────────────────────────────────────────────
def subsets_backtrack(nums: list[int]) -> list[list[int]]:
    """Backtracking: include/exclude each element."""
    result: list[list[int]] = []

    def backtrack(idx: int, current: list[int]) -> None:
        if idx == len(nums):
            result.append(current[:])
            return
        # Exclude nums[idx]
        backtrack(idx + 1, current)
        # Include nums[idx]
        current.append(nums[idx])
        backtrack(idx + 1, current)
        current.pop()

    backtrack(0, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: Iterative cascading
# Time: O(N × 2^N)
# Space: O(2^N) for output.
# ──────────────────────────────────────────────────────────────────────────────
def subsets_iterative(nums: list[int]) -> list[list[int]]:
    """Build subsets iteratively by adding each num to existing subsets."""
    result: list[list[int]] = [[]]
    for num in nums:
        result += [curr + [num] for curr in result]
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, nums: list[int], expected: list[list[int]]):
        methods = [
            ("Backtrack", subsets_backtrack),
            ("Iterative", subsets_iterative),
        ]
        for name, fn in methods:
            result = fn(nums[:])
            result_set = {frozenset(s) for s in result}
            expected_set = {frozenset(s) for s in expected}
            ok = result_set == expected_set and len(result) == len(expected)
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {len(result)} subsets)")

    test("Example 1", [1, 2, 3],
         [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
    test("Example 2", [0], [[], [0]])
    test("Empty", [], [[]])
    print("\nAll subsets tests completed.")
