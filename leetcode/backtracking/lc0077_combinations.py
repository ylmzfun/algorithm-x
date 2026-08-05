"""
77. Combinations
https://leetcode.com/problems/combinations/

Given two integers n and k, return all possible combinations of k numbers
chosen from the range [1, n]. You may return the answer in any order.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking
# Iterate from `start` to n, adding each candidate and recursing with
# `start+1`. Prune when remaining numbers are insufficient.
# Time: O(C(n, k) × k) — C(n,k) combinations, each size k.
# Space: O(k) recursion depth.
# ──────────────────────────────────────────────────────────────────────────────
def combine(n: int, k: int) -> list[list[int]]:
    """Generate all C(n, k) combinations."""
    result: list[list[int]] = []

    def backtrack(start: int, current: list[int]) -> None:
        if len(current) == k:
            result.append(current[:])
            return
        # Pruning: need (k - len(current)) more numbers
        # Last possible start = n - (k - len(current)) + 1
        for i in range(start, n - (k - len(current)) + 2):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, n: int, k: int, expected: list[list[int]]):
        result = combine(n, k)
        result_set = {tuple(c) for c in result}
        expected_set = {tuple(c) for c in expected}
        ok = result_set == expected_set and len(result) == len(expected)
        print(f"[{label}] {'✓' if ok else '✗'} (got {len(result)} combos)")

    test("Example 1", 4, 2,
         [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]])
    test("Example 2", 1, 1, [[1]])
    test("n=5 k=3", 5, 3,
         [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5],
          [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]])
    print("\nAll combinations tests completed.")
