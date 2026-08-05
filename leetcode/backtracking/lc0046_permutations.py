"""
46. Permutations
https://leetcode.com/problems/permutations/

Given an array nums of distinct integers, return all the possible
permutations. You can return the answer in any order.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Backtracking with used[] array
# Time: O(N × N!) — N! permutations, each takes O(N) to copy.
# Space: O(N) recursion depth + O(N) used array.
# ──────────────────────────────────────────────────────────────────────────────
def permute_backtrack(nums: list[int]) -> list[list[int]]:
    """Backtracking with boolean used array."""
    result: list[list[int]] = []
    n = len(nums)
    used = [False] * n

    def backtrack(current: list[int]) -> None:
        if len(current) == n:
            result.append(current[:])
            return
        for i, num in enumerate(nums):
            if not used[i]:
                used[i] = True
                current.append(num)
                backtrack(current)
                current.pop()
                used[i] = False

    backtrack([])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: In-place swap
# Time: O(N × N!)
# Space: O(N) recursion depth (no extra array for used).
# ──────────────────────────────────────────────────────────────────────────────
def permute_swap(nums: list[int]) -> list[list[int]]:
    """In-place swapping to generate permutations."""
    result: list[list[int]] = []
    n = len(nums)

    def backtrack(start: int) -> None:
        if start == n:
            result.append(nums[:])
            return
        for i in range(start, n):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # backtrack

    backtrack(0)
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, nums: list[int], expected: list[list[int]]):
        methods = [
            ("Backtrack", permute_backtrack),
            ("Swap", permute_swap),
        ]
        for name, fn in methods:
            result = fn(nums[:])
            result_set = {tuple(p) for p in result}
            expected_set = {tuple(p) for p in expected}
            ok = result_set == expected_set
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {len(result)} perms)")

    test("Example 1", [1, 2, 3],
         [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    test("Example 2", [0, 1], [[0, 1], [1, 0]])
    test("Example 3", [1], [[1]])
    print("\nAll permutations tests completed.")
