"""
40. Combination Sum II
https://leetcode.com/problems/combination-sum-ii/

Given a collection of candidate numbers (candidates) and a target number
(target), find all unique combinations in candidates where the candidate
numbers sum to target.

Each number in candidates may only be used once in the combination.
Note: The solution set must not contain duplicate combinations.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with sorting and duplicate skipping
# Sort candidates. At each recursion depth, skip same-valued candidates in
# the same loop iteration to avoid duplicates across the same position.
# Time: O(2^N) worst — each element included/excluded; heavily pruned.
# Space: O(N) recursion depth.
# ──────────────────────────────────────────────────────────────────────────────
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    """Backtracking with skip of same-value candidates at same depth."""
    candidates.sort()
    result: list[list[int]] = []

    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            # Skip duplicates at the same recursion level
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            c = candidates[i]
            if c > remaining:
                break
            current.append(c)
            backtrack(i + 1, remaining - c, current)  # i+1: no reuse
            current.pop()

    backtrack(0, target, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, candidates: list[int], target: int,
             expected: list[list[int]]):
        result = combination_sum2(candidates, target)
        result_set = {tuple(sorted(c)) for c in result}
        expected_set = {tuple(sorted(c)) for c in expected}
        ok = result_set == expected_set
        print(f"[{label}] {'✓' if ok else '✗'} (got {result})")

    test("Example 1", [10, 1, 2, 7, 6, 1, 5], 8,
         [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]])
    test("Example 2", [2, 5, 2, 1, 2], 5, [[1, 2, 2], [5]])
    test("Empty result", [2], 1, [])
    print("\nAll combination sum II tests completed.")
