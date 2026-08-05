"""
LeetCode #215: Kth Largest Element in an Array
https://leetcode.com/problems/kth-largest-element-in-an-array/

Given an integer array `nums` and an integer `k`, return the k-th largest element
in the array. Note that it is the k-th largest element in sorted order, not the
k-th distinct element.

Can you solve it without sorting?

Constraints:
- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Approach 1: Quickselect (Hoare's Selection Algorithm)
    Partition the array around a pivot. If pivot index == n - k, return it.
    Otherwise recurse on the appropriate partition.
    Average O(n) time, worst-case O(n^2), O(1) space.

Approach 2: Min-Heap of size k
    Maintain a heap of the k largest elements. After processing all elements,
    the top of the min-heap is the k-th largest.
    O(n log k) time, O(k) space.

Approach 3: Sorting
    Sort and return nums[n - k]. O(n log n) time, O(1) space.
"""

from typing import List
import heapq
import random


def find_kth_largest_quickselect(nums: List[int], k: int) -> int:
    """Quickselect: average O(n) time, O(1) space."""
    target = len(nums) - k

    def partition(left: int, right: int, pivot_idx: int) -> int:
        pivot_val = nums[pivot_idx]
        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot_val:
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1
        # Move pivot to its final place
        nums[right], nums[store_idx] = nums[store_idx], nums[right]
        return store_idx

    def select(left: int, right: int) -> int:
        if left == right:
            return nums[left]

        # Random pivot for average-case performance
        pivot_idx = random.randint(left, right)
        pivot_idx = partition(left, right, pivot_idx)

        if pivot_idx == target:
            return nums[pivot_idx]
        elif pivot_idx < target:
            return select(pivot_idx + 1, right)
        else:
            return select(left, pivot_idx - 1)

    return select(0, len(nums) - 1)


def find_kth_largest_heap(nums: List[int], k: int) -> int:
    """Min-heap of size k: O(n log k) time, O(k) space."""
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]


# ── Default export ──
findKthLargest = find_kth_largest_quickselect


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        ([1], 1, 1),
        ([7, 6, 5, 4, 3, 2, 1], 5, 3),
        ([5, 2, 4, 1, 3, 6, 0], 4, 3),
    ]

    all_pass = True
    for nums, k, expected in test_cases:
        r1 = find_kth_largest_quickselect(nums[:], k)
        r2 = find_kth_largest_heap(nums[:], k)
        pass_flag = r1 == expected and r2 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums}, k={k} => qs={r1}, heap={r2} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
