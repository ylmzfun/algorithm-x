"""
39. Combination Sum
https://leetcode.com/problems/combination-sum/

Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen
numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with index pruning
# Sort candidates first. At each index, either include the current number
# (stay at same index for unlimited reuse) or skip to the next.
# Time: O(N^(T/M)) where T=target, M=min(candidates); heavily pruned.
# Space: O(T/M) recursion depth.
# ──────────────────────────────────────────────────────────────────────────────
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """Backtracking: reuse elements by staying at same index."""
    candidates.sort()
    result: list[list[int]] = []

    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remaining:
                break  # sorted, so further candidates will also exceed
            current.append(c)
            backtrack(i, remaining - c, current)  # i, not i+1, for reuse
            current.pop()

    backtrack(0, target, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, candidates: list[int], target: int,
             expected: list[list[int]]):
        result = combination_sum(candidates, target)
        result_set = {tuple(sorted(c)) for c in result}
        expected_set = {tuple(sorted(c)) for c in expected}
        ok = result_set == expected_set
        print(f"[{label}] {'✓' if ok else '✗'} (got {result})")

    test("Example 1", [2, 3, 6, 7], 7, [[2, 2, 3], [7]])
    test("Example 2", [2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]])
    test("Example 3", [2], 1, [])
    print("\nAll combination sum tests completed.")
