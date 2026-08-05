"""
LeetCode #39: Combination Sum
https://leetcode.com/problems/combination-sum/

Given an array of distinct integers `candidates` and a target integer `target`, return
a list of all unique combinations of candidates where the chosen numbers sum to target.
You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two
combinations are unique if the frequency of at least one of the chosen numbers
is different.

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct.
- 1 <= target <= 500

Approach: Backtracking
    Standard backtracking with a start index to avoid duplicate combinations.
    Since elements can be reused, the recursive call uses the same start index.
    Explore by including candidates[i] and subtracting from target.
    O(2^t) time where t = target/min(candidates), O(t) recursion depth.
"""

from typing import List


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """Backtracking: O(2^t) time, O(t) recursion depth ignoring output."""
    result: List[List[int]] = []

    def backtrack(start: int, remaining: int, path: List[int]) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return

        for i in range(start, len(candidates)):
            # Optimization: if candidates are sorted, we can prune
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i], path)  # i not i+1 (unlimited reuse)
            path.pop()

    candidates.sort()  # Sort for pruning (optional but helps)
    backtrack(0, target, [])
    return result


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([2, 3, 6, 7], 7, [[2, 2, 3], [7]]),
        ([2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
        ([2], 1, []),
        ([1], 1, [[1]]),
        ([1], 2, [[1, 1]]),
    ]

    all_pass = True
    for candidates, target, expected in test_cases:
        result = combination_sum(candidates, target)
        result_sorted = sorted([sorted(c) for c in result])
        expected_sorted = sorted([sorted(c) for c in expected])
        pass_flag = result_sorted == expected_sorted
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | candidates={candidates}, target={target} => {result}")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
