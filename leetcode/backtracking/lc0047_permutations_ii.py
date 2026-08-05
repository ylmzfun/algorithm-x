"""
47. Permutations II
https://leetcode.com/problems/permutations-ii/

Given a collection of numbers, nums, that might contain duplicates, return
all possible unique permutations in any order.
"""

from __future__ import annotations
from collections import Counter


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Backtracking with frequency counter
# Use a Counter to track remaining usage of each number.
# Time: O(N × N!) worst — duplicates reduce the effective count.
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def permute_unique_counter(nums: list[int]) -> list[list[int]]:
    """Backtracking using a frequency counter to handle duplicates."""
    freq = Counter(nums)
    result: list[list[int]] = []

    def backtrack(current: list[int]) -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for num in freq:
            if freq[num] > 0:
                freq[num] -= 1
                current.append(num)
                backtrack(current)
                current.pop()
                freq[num] += 1

    backtrack([])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: Backtracking with used[] and sorting
# Time: O(N × N!)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def permute_unique_sort(nums: list[int]) -> list[list[int]]:
    """Sort + used array, skip duplicate at same recursion level."""
    nums.sort()
    result: list[list[int]] = []
    n = len(nums)
    used = [False] * n

    def backtrack(current: list[int]) -> None:
        if len(current) == n:
            result.append(current[:])
            return
        for i in range(n):
            if used[i]:
                continue
            # Skip duplicate: if same as previous and previous not used
            # in this recursion path, it would create duplicates.
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False

    backtrack([])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, nums: list[int], expected: list[list[int]]):
        methods = [
            ("Counter", permute_unique_counter),
            ("Sort", permute_unique_sort),
        ]
        for name, fn in methods:
            result = fn(nums[:])
            result_set = {tuple(p) for p in result}
            expected_set = {tuple(p) for p in expected}
            ok = result_set == expected_set and len(result) == len(expected)
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {len(result)} perms, expected {len(expected)})")

    test("Example 1", [1, 1, 2], [[1, 1, 2], [1, 2, 1], [2, 1, 1]])
    test("Example 2", [1, 2, 3],
         [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    test("All same", [1, 1, 1], [[1, 1, 1]])
    print("\nAll permutations II tests completed.")
