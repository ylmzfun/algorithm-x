"""
LeetCode #84: Largest Rectangle in Histogram
https://leetcode.com/problems/largest-rectangle-in-histogram/

Given an array of integers `heights` representing the histogram's bar height where
the width of each bar is 1, return the area of the largest rectangle in the histogram.

Constraints:
- 1 <= heights.length <= 10^5
- 0 <= heights[i] <= 10^4

Approach 1: Monotonic Stack
    For each bar, find the nearest smaller bar on the left and right.
    Area = height[i] * (right_boundary - left_boundary - 1).
    Use a monotonic increasing stack storing indices.
    O(n) time, O(n) space.

Approach 2: Brute Force
    For each bar, expand left and right. O(n^2) time, O(1) space.
"""

from typing import List


def largest_rectangle_area_stack(heights: List[int]) -> int:
    """Monotonic stack: O(n) time, O(n) space."""
    stack: List[int] = []  # Stores indices of bars in increasing height order
    max_area = 0

    # Append a sentinel 0 at the end to flush the stack
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            # If stack is empty, width extends to the start
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area


def largest_rectangle_area_brute(heights: List[int]) -> int:
    """Brute force: O(n^2) time, O(1) space."""
    n = len(heights)
    max_area = 0
    for i in range(n):
        # Expand right
        left = i
        while left > 0 and heights[left - 1] >= heights[i]:
            left -= 1
        right = i
        while right < n - 1 and heights[right + 1] >= heights[i]:
            right += 1
        max_area = max(max_area, heights[i] * (right - left + 1))
    return max_area


# ── Default export ──
largestRectangleArea = largest_rectangle_area_stack


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([2, 1, 5, 6, 2, 3], 10),
        ([2, 4], 4),
        ([1], 1),
        ([0, 0, 0], 0),
        ([4, 2, 0, 3, 2, 5], 6),
    ]

    all_pass = True
    for heights, expected in test_cases:
        r1 = largest_rectangle_area_stack(heights)
        pass_flag = r1 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | heights={heights} => {r1} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
