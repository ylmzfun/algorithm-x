"""
LeetCode #239: Sliding Window Maximum
https://leetcode.com/problems/sliding-window-maximum/

You are given an array of integers `nums` and a sliding window of size `k` moving
from the very left of the array to the right. You can only see the k numbers in the
window. Each time the window moves right by one position, return the max value in
the window.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- 1 <= k <= nums.length

Approach 1: Monotonic Deque (Decreasing)
    Maintain a deque of indices where values are in strictly decreasing order.
    Front of deque is the max for the current window. Remove elements outside
    the window from the front, and remove smaller elements from the back.
    O(n) time, O(k) space.

Approach 2: Heap
    Max-heap of (value, index); pop elements outside window. O(n log n) time.
"""

from typing import List
from collections import deque
import heapq


def max_sliding_window_deque(nums: List[int], k: int) -> List[int]:
    """Monotonic deque: O(n) time, O(k) space."""
    dq: deque[int] = deque()  # Stores indices, values in decreasing order
    result: List[int] = []

    for i, num in enumerate(nums):
        # Remove elements outside the current window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove smaller elements from the back
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Add to result once the first window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def max_sliding_window_heap(nums: List[int], k: int) -> List[int]:
    """Max-heap: O(n log n) time, O(n) space."""
    if not nums:
        return []

    # Python has min-heap; use negative values for max-heap
    heap: List[tuple[int, int]] = []
    result: List[int] = []

    for i, num in enumerate(nums):
        heapq.heappush(heap, (-num, i))
        # Remove elements outside the window
        while heap[0][1] <= i - k:
            heapq.heappop(heap)
        if i >= k - 1:
            result.append(-heap[0][0])

    return result


# ── Default export ──
maxSlidingWindow = max_sliding_window_deque


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1], 1, [1]),
        ([1, -1], 1, [1, -1]),
        ([9, 11], 2, [11]),
        ([4, -2], 2, [4]),
    ]

    all_pass = True
    for nums, k, expected in test_cases:
        r1 = max_sliding_window_deque(nums, k)
        r2 = max_sliding_window_heap(nums, k)
        pass_flag = r1 == expected and r2 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums}, k={k} => dq={r1}, heap={r2} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
