"""
216. Combination Sum III
https://leetcode.com/problems/combination-sum-iii/

Find all valid combinations of k numbers that sum up to n such that the
following conditions are true:
- Only numbers 1 through 9 are used.
- Each number is used at most once.

Return a list of all possible valid combinations.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking
# Same as combinations but with a target sum constraint. Prune when
# remaining sum is insufficient or exceeded.
# Time: O(C(9, k) × k) — choose k from 9; pruned by sum.
# Space: O(k)
# ──────────────────────────────────────────────────────────────────────────────
def combination_sum3(k: int, n: int) -> list[list[int]]:
    """Backtrack: choose k numbers from 1-9 summing to n."""
    result: list[list[int]] = []

    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if len(current) == k:
            if remaining == 0:
                result.append(current[:])
            return
        # Pruning: remaining numbers needed = k - len(current)
        # Max sum we can still make with remaining numbers from start to 9
        # (sum of last (k - len(current)) numbers)
        needed = k - len(current)
        if remaining < 0 or start > 9 - needed + 1:
            return

        for i in range(start, 10):
            if i > remaining and current:
                # Numbers only increase; if current smallest candidate > remaining, stop
                break
            current.append(i)
            backtrack(i + 1, remaining - i, current)
            current.pop()

    backtrack(1, n, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, k: int, n: int, expected: list[list[int]]):
        result = combination_sum3(k, n)
        result_set = {tuple(sorted(c)) for c in result}
        expected_set = {tuple(sorted(c)) for c in expected}
        ok = result_set == expected_set and len(result) == len(expected)
        print(f"[{label}] {'✓' if ok else '✗'} (got {len(result)} combos)")

    test("Example 1", 3, 7, [[1, 2, 4]])
    test("Example 2", 3, 9, [[1, 2, 6], [1, 3, 5], [2, 3, 4]])
    test("Example 3", 4, 1, [])
    test("k=1", 1, 5, [[5]])
    print("\nAll combination sum III tests completed.")
