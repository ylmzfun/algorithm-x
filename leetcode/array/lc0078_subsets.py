"""
LeetCode #78: Subsets
https://leetcode.com/problems/subsets/

Given an integer array `nums` of unique elements, return all possible subsets
(the power set). The solution set must not contain duplicate subsets. You may return
the answer in any order.

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique.

Approach 1: Backtracking
    For each element, decide to include or exclude it. Build subsets recursively.
    O(n * 2^n) time, O(n) recursion depth.

Approach 2: Iterative (Cascading)
    Start with [[]], then for each num, append num to every existing subset.
    O(n * 2^n) time, O(1) extra space (ignoring output).
"""

from typing import List


def subsets_backtrack(nums: List[int]) -> List[List[int]]:
    """Backtracking: O(n * 2^n) time."""
    result: List[List[int]] = []

    def backtrack(start: int, path: List[int]) -> None:
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def subsets_iterative(nums: List[int]) -> List[List[int]]:
    """Iterative cascading: O(n * 2^n) time."""
    result: List[List[int]] = [[]]

    for num in nums:
        new_subsets = [subset + [num] for subset in result]
        result.extend(new_subsets)

    return result


# ── Default export ──
subsets = subsets_backtrack


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3], [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]),
        ([0], [[], [0]]),
        ([1, 2], [[], [1], [2], [1, 2]]),
    ]

    all_pass = True
    for nums, expected in test_cases:
        r1 = subsets_backtrack(nums)
        r2 = subsets_iterative(nums)
        r1_sorted = sorted([sorted(s) for s in r1])
        r2_sorted = sorted([sorted(s) for s in r2])
        expected_sorted = sorted([sorted(s) for s in expected])
        pass_flag = r1_sorted == expected_sorted and r2_sorted == expected_sorted
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => back={r1_sorted}, iter={r2_sorted}")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
