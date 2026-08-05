"""
Sorting-Related Classic Problems
=================================

Problems that are solved elegantly using sorting techniques or partitioning:

- sort_colors           : Dutch national flag – in-place three-way partition.
- find_kth_largest      : Quickselect – O(n) average.
- merge_intervals       : Merge overlapping intervals.
- sort_nearly_sorted    : Sort an array where each element is at most k
                          positions away from its target (min-heap).
"""

import heapq
import random
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Sort Colors (Dutch National Flag)
# ---------------------------------------------------------------------------

def sort_colors(nums: List[int]) -> None:
    """
    Sort an array of 0s, 1s, and 2s in-place (Dutch national flag problem).

    Uses three-way partitioning with three pointers: lo, mid, hi.

    Parameters
    ----------
    nums : List[int]
        List containing only values 0, 1, and 2.  Modified in place.

    Time  : O(n)
    Space : O(1)

    Example
    -------
    >>> arr = [2, 0, 2, 1, 1, 0]
    >>> sort_colors(arr)
    >>> arr
    [0, 0, 1, 1, 2, 2]
    """
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1


# ---------------------------------------------------------------------------
# Kth Largest Element (Quickselect)
# ---------------------------------------------------------------------------

def _partition(nums: List[int], lo: int, hi: int) -> int:
    """Lomuto partition with random pivot.  Returns pivot index."""
    pivot_idx = random.randint(lo, hi)
    nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]
    pivot = nums[hi]
    i = lo
    for j in range(lo, hi):
        if nums[j] <= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[hi] = nums[hi], nums[i]
    return i


def find_kth_largest(nums: List[int], k: int) -> int:
    """
    Find the k-th largest element in an unsorted list using quickselect.

    Parameters
    ----------
    nums : List[int]
        Unsorted list of integers.
    k : int
        1-indexed: k=1 returns the largest, k=2 the second largest, etc.

    Returns
    -------
    int
        The k-th largest element.

    Time  : O(n) average, O(n²) worst-case.
    Space : O(1) auxiliary.

    Raises
    ------
    ValueError
        If k is out of range [1, len(nums)].

    Example
    -------
    >>> find_kth_largest([3, 2, 1, 5, 6, 4], 2)
    5
    """
    if not 1 <= k <= len(nums):
        raise ValueError(f"k={k} out of range [1, {len(nums)}]")

    target = len(nums) - k  # zero-based index of k-th largest
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        p = _partition(nums, lo, hi)
        if p == target:
            return nums[p]
        elif p < target:
            lo = p + 1
        else:
            hi = p - 1
    return -1  # unreachable


# ---------------------------------------------------------------------------
# Merge Intervals
# ---------------------------------------------------------------------------

def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge all overlapping intervals and return a list of non-overlapping
    intervals that cover all the original intervals.

    Parameters
    ----------
    intervals : List[Tuple[int, int]]
        List of (start, end) intervals.  Not necessarily sorted.

    Returns
    -------
    List[Tuple[int, int]]
        Merged, non-overlapping intervals sorted by start.

    Time  : O(n log n) — dominated by sorting.
    Space : O(n) for output (or O(1) if output overwrites input).

    Example
    -------
    >>> merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)])
    [(1, 6), (8, 10), (15, 18)]
    """
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged: List[Tuple[int, int]] = [sorted_intervals[0]]

    for start, end in sorted_intervals[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))

    return merged


# ---------------------------------------------------------------------------
# Sort a Nearly-Sorted (K-sorted) Array
# ---------------------------------------------------------------------------

def sort_nearly_sorted(arr: List[int], k: int) -> List[int]:
    """
    Sort a nearly-sorted (k-sorted) array where each element is at most k
    positions away from its correct sorted position.

    Uses a min-heap of size k+1.

    Parameters
    ----------
    arr : List[int]
        The nearly-sorted array.
    k : int
        Maximum displacement of any element from its sorted position.

    Returns
    -------
    List[int]
        A new fully-sorted list.

    Time  : O(n log k).
    Space : O(k).

    Example
    -------
    >>> sort_nearly_sorted([6, 5, 3, 2, 8, 10, 9], 3)
    [2, 3, 5, 6, 8, 9, 10]
    """
    n = len(arr)
    result: List[int] = []
    heap: List[int] = []

    # Push first k+1 elements into the heap
    for i in range(min(k + 1, n)):
        heapq.heappush(heap, arr[i])

    # For each remaining element, pop min and push next
    for i in range(k + 1, n):
        result.append(heapq.heappop(heap))
        heapq.heappush(heap, arr[i])

    # Drain the heap
    while heap:
        result.append(heapq.heappop(heap))

    return result


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Sort Problems Tests ===\n")

    # --- sort_colors ---
    tests_ok = True
    cases = [
        ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]),
        ([2, 0, 1], [0, 1, 2]),
        ([0], [0]),
        ([], []),
        ([1, 1, 1], [1, 1, 1]),
        ([2, 2, 0, 0], [0, 0, 2, 2]),
    ]
    for arr, expected in cases:
        a = arr[:]
        sort_colors(a)
        if a != expected:
            print(f"  FAIL sort_colors: {arr} -> {a}, expected {expected}")
            tests_ok = False
    if tests_ok:
        print("  PASS sort_colors")

    # --- find_kth_largest ---
    tests_ok = True
    cases = [
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        ([1], 1, 1),
        ([7, 6, 5, 4, 3, 2, 1], 5, 3),
    ]
    for arr, k, expected in cases:
        result = find_kth_largest(arr[:], k)
        if result != expected:
            print(f"  FAIL find_kth_largest: arr={arr}, k={k} -> {result}, expected {expected}")
            tests_ok = False
    if tests_ok:
        print("  PASS find_kth_largest")

    try:
        find_kth_largest([1, 2], 3)
        print("  FAIL find_kth_largest: should raise ValueError")
    except ValueError:
        print("  PASS find_kth_largest: ValueError for invalid k")

    # --- merge_intervals ---
    tests_ok = True
    cases = [
        ([(1, 3), (2, 6), (8, 10), (15, 18)], [(1, 6), (8, 10), (15, 18)]),
        ([(1, 4), (4, 5)], [(1, 5)]),
        ([(1, 4), (2, 3)], [(1, 4)]),
        ([(1, 2), (3, 4)], [(1, 2), (3, 4)]),
        ([], []),
    ]
    for intervals, expected in cases:
        result = merge_intervals(intervals[:])
        if result != expected:
            print(f"  FAIL merge_intervals: {intervals} -> {result}, expected {expected}")
            tests_ok = False
    if tests_ok:
        print("  PASS merge_intervals")

    # --- sort_nearly_sorted ---
    tests_ok = True
    cases = [
        ([6, 5, 3, 2, 8, 10, 9], 3, [2, 3, 5, 6, 8, 9, 10]),
        ([10, 9, 8, 7, 4, 70, 60, 50], 4, [4, 7, 8, 9, 10, 50, 60, 70]),
        ([1, 2, 3, 4], 1, [1, 2, 3, 4]),
        ([1], 0, [1]),
        ([], 1, []),
    ]
    for arr, k, expected in cases:
        result = sort_nearly_sorted(arr[:], k)
        if result != expected:
            print(f"  FAIL sort_nearly_sorted: {arr}, k={k} -> {result}, expected {expected}")
            tests_ok = False
    if tests_ok:
        print("  PASS sort_nearly_sorted")

    print("\nAll sort problem tests completed!")
