"""
LeetCode #11: Container With Most Water
https://leetcode.com/problems/container-with-most-water/

You are given an integer array `height` of length n. There are n vertical lines drawn
such that the two endpoints of the i-th line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container
contains the most water. Return the maximum amount of water a container can store.

Constraints:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4

Approach 1: Brute Force
    Check every pair of lines. O(n^2) time, O(1) space.

Approach 2: Two Pointers
    Start with left = 0, right = n - 1. The area is determined by the shorter line.
    Move the pointer pointing to the shorter line inward, as moving the taller line
    can never increase the area. O(n) time, O(1) space.
"""

from typing import List


def max_area_brute(height: List[int]) -> int:
    """Brute force: O(n^2) time, O(1) space."""
    n = len(height)
    max_w = 0
    for i in range(n):
        for j in range(i + 1, n):
            water = min(height[i], height[j]) * (j - i)
            max_w = max(max_w, water)
    return max_w


def max_area_two_pointer(height: List[int]) -> int:
    """Two-pointer approach: O(n) time, O(1) space."""
    left, right = 0, len(height) - 1
    max_w = 0

    while left < right:
        h = min(height[left], height[right])
        w = right - left
        max_w = max(max_w, h * w)

        # Move the pointer that points to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_w


# ── Default export ──
maxArea = max_area_two_pointer


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
        ([2, 3, 10, 5, 7, 8, 9], 36),
    ]

    all_pass = True
    for height, expected in test_cases:
        result = max_area_two_pointer(height)
        pass_flag = result == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | height={height} => {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
