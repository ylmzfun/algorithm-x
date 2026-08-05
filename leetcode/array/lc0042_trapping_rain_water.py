"""
LeetCode #42: Trapping Rain Water
https://leetcode.com/problems/trapping-rain-water/

Given `n` non-negative integers representing an elevation map where the width of
each bar is 1, compute how much water it can trap after raining.

Constraints:
- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5

Approach 1: Two Pointers
    Use left and right pointers with left_max and right_max trackers.
    At each step, the water at a position is determined by the smaller of the
    max heights on either side. O(n) time, O(1) space.

Approach 2: Monotonic Stack
    Push decreasing heights onto a stack; when a taller bar is encountered,
    pop and calculate trapped water in the basin. O(n) time, O(n) space.

Approach 3: Dynamic Programming
    Precompute left_max and right_max for each position, then sum water.
    O(n) time, O(n) space.
"""

from typing import List


def trap_two_pointer(height: List[int]) -> int:
    """Two-pointer approach: O(n) time, O(1) space."""
    if not height:
        return 0

    left, right = 0, len(height) - 1
    left_max = height[left]
    right_max = height[right]
    water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]

    return water


def trap_stack(height: List[int]) -> int:
    """Monotonic stack approach: O(n) time, O(n) space."""
    stack: List[int] = []  # Store indices
    water = 0

    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            w = i - left - 1
            bounded_h = min(height[left], h) - height[bottom]
            water += w * bounded_h

        stack.append(i)

    return water


# ── Default export ──
trap = trap_two_pointer


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([1], 0),
        ([2, 1, 2], 1),
        ([4, 2, 3], 1),
    ]

    all_pass = True
    for h, expected in test_cases:
        r1 = trap_two_pointer(h)
        r2 = trap_stack(h)
        pass_flag = r1 == expected and r2 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | height={h} => two_ptr={r1}, stack={r2} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
