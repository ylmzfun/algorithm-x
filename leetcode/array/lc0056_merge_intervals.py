"""
LeetCode #56: Merge Intervals
https://leetcode.com/problems/merge-intervals/

Given an array of `intervals` where intervals[i] = [start_i, end_i], merge all
overlapping intervals, and return an array of the non-overlapping intervals that
cover all the intervals in the input.

Constraints:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^4

Approach: Sort + Linear Scan
    Sort intervals by start time. Iterate through sorted intervals, merging
    overlapping ones into the current result. O(n log n) time, O(n) space for output.
"""

from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    """Sort + linear scan: O(n log n) time, O(n) space."""
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    merged: List[List[int]] = [intervals[0]]

    for start, end in intervals[1:]:
        prev_end = merged[-1][1]
        if start <= prev_end:
            # Overlapping → merge by extending the end
            merged[-1][1] = max(prev_end, end)
        else:
            # No overlap → add as new interval
            merged.append([start, end])

    return merged


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([[1, 4], [0, 4]], [[0, 4]]),
        ([[1, 4], [0, 0]], [[0, 0], [1, 4]]),
        ([[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]], [[1, 10]]),
    ]

    all_pass = True
    for intervals, expected in test_cases:
        result = merge(intervals)
        pass_flag = result == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | intervals={intervals} => {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
