"""
Binary Search Applications
===========================

This module demonstrates how binary search can be applied beyond simple
lookup to solve non-trivial algorithmic problems.

Problems:
- search_rotated_sorted    : Search in a rotated sorted array (no duplicates).
- find_peak_element        : Find a peak in an unsorted array.
- find_min_rotated         : Minimum in a rotated sorted array.
- search_2d_matrix         : Search in a row- and column-sorted 2D matrix.
- sqrt_binary_search       : Integer square root via binary search.
- ship_within_days         : Capacity to ship packages within D days.
- split_array_largest_sum  : Split array into m sub-arrays minimising the
                              largest sum.
"""

from typing import List, Optional


# ---------------------------------------------------------------------------
# Search in Rotated Sorted Array
# ---------------------------------------------------------------------------

def search_rotated_sorted(nums: List[int], target: int) -> int:
    """
    Search for ``target`` in a sorted array that has been rotated at an
    unknown pivot index.  Assumes all values are distinct.

    Parameters
    ----------
    nums : List[int]
        Rotated sorted array with distinct values.
    target : int
        Value to find.

    Returns
    -------
    int
        Index of ``target``, or -1 if not found.

    Time  : O(log n)
    Space : O(1)

    Example
    -------
    >>> search_rotated_sorted([4, 5, 6, 7, 0, 1, 2], 0)
    4
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid

        # Determine which half is sorted
        if nums[lo] <= nums[mid]:  # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


# ---------------------------------------------------------------------------
# Find Peak Element
# ---------------------------------------------------------------------------

def find_peak_element(nums: List[int]) -> int:
    """
    Find a peak element in an array.  An element is a peak if it is greater
    than or equal to its neighbours (nums[-1] = nums[n] = -inf).

    Returns any peak index.  Multiple valid answers are possible.

    Parameters
    ----------
    nums : List[int]
        Array of integers.

    Returns
    -------
    int
        Index of a peak element.

    Time  : O(log n)
    Space : O(1)

    Example
    -------
    >>> find_peak_element([1, 2, 3, 1])
    2
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------------------
# Find Minimum in Rotated Sorted Array
# ---------------------------------------------------------------------------

def find_min_rotated(nums: List[int]) -> int:
    """
    Find the minimum element in a rotated sorted array with distinct values.

    Parameters
    ----------
    nums : List[int]
        Rotated sorted array (no duplicates).

    Returns
    -------
    int
        The minimum value.

    Time  : O(log n)
    Space : O(1)

    Example
    -------
    >>> find_min_rotated([3, 4, 5, 1, 2])
    1
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


# ---------------------------------------------------------------------------
# Search a 2D Matrix
# ---------------------------------------------------------------------------

def search_2d_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    Search for ``target`` in an m×n matrix where:
      * Each row is sorted in ascending order.
      * The first element of each row is greater than the last element of the
        previous row.

    Approach: treat the 2D matrix as a flat 1D sorted array.

    Parameters
    ----------
    matrix : List[List[int]]
        The sorted 2D matrix.
    target : int
        Value to find.

    Returns
    -------
    bool
        True if ``target`` exists in the matrix.

    Time  : O(log(m·n))
    Space : O(1)
    """
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        val = matrix[mid // cols][mid % cols]
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


# ---------------------------------------------------------------------------
# Integer Square Root
# ---------------------------------------------------------------------------

def sqrt_binary_search(x: int) -> int:
    """
    Compute the integer square root of a non-negative integer x,
    i.e. the largest integer r such that r² ≤ x.

    Parameters
    ----------
    x : int
        Non-negative integer.

    Returns
    -------
    int
        Floor of √x.

    Time  : O(log x)
    Space : O(1)

    Example
    -------
    >>> sqrt_binary_search(8)
    2
    >>> sqrt_binary_search(9)
    3
    """
    if x < 2:
        return x
    lo, hi = 1, x // 2
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        sq = mid * mid
        if sq == x:
            return mid
        elif sq < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi


# ---------------------------------------------------------------------------
# Capacity to Ship Packages Within D Days
# ---------------------------------------------------------------------------

def _days_needed(weights: List[int], capacity: int) -> int:
    """Compute days required to ship all packages with given capacity."""
    days = 1
    cur = 0
    for w in weights:
        if cur + w > capacity:
            days += 1
            cur = w
        else:
            cur += w
    return days


def ship_within_days(weights: List[int], days: int) -> int:
    """
    Find the minimum ship capacity such that all packages can be shipped
    within the given number of days.  Packages must be shipped in the given
    order.

    Parameters
    ----------
    weights : List[int]
        Weights of packages in order.
    days : int
        Maximum number of days allowed.

    Returns
    -------
    int
        Minimum ship capacity.

    Time  : O(n log(sum(weights)))
    Space : O(1)

    Example
    -------
    >>> ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
    15
    """
    lo = max(weights)  # minimum capacity = heaviest single package
    hi = sum(weights)  # maximum capacity = ship everything in one day
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if _days_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---------------------------------------------------------------------------
# Split Array Largest Sum
# ---------------------------------------------------------------------------

def _count_splits(nums: List[int], max_sum: int) -> int:
    """Count how many sub-arrays are needed with the given max_sum limit."""
    splits = 1
    cur = 0
    for x in nums:
        if cur + x > max_sum:
            splits += 1
            cur = x
        else:
            cur += x
    return splits


def split_array_largest_sum(nums: List[int], m: int) -> int:
    """
    Split the array ``nums`` into ``m`` contiguous sub-arrays such that the
    largest sum among them is minimised.  Return that minimised largest sum.

    Parameters
    ----------
    nums : List[int]
        Array of non-negative integers.
    m : int
        Number of sub-arrays to split into.

    Returns
    -------
    int
        Minimised largest sub-array sum.

    Time  : O(n log(sum(nums)))
    Space : O(1)

    Example
    -------
    >>> split_array_largest_sum([7, 2, 5, 10, 8], 2)
    18
    """
    lo = max(nums)
    hi = sum(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if _count_splits(nums, mid) <= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Binary Search Applications Tests ===\n")

    # search_rotated_sorted
    cases = [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([1], 0, -1),
        ([1], 1, 0),
        ([3, 1], 1, 1),
    ]
    ok = True
    for nums, tgt, exp in cases:
        res = search_rotated_sorted(nums, tgt)
        if res != exp:
            print(f"  FAIL search_rotated_sorted {nums}, {tgt} -> {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} search_rotated_sorted")

    # find_peak_element
    cases = [
        ([1, 2, 3, 1], [2]),
        ([1, 2, 1, 3, 5, 6, 4], [1, 5]),
        ([1], [0]),
        ([1, 2], [1]),
    ]
    ok = True
    for nums, valid in cases:
        idx = find_peak_element(nums)
        n = len(nums)
        left_ok = (idx == 0) or (nums[idx] >= nums[idx - 1])
        right_ok = (idx == n - 1) or (nums[idx] >= nums[idx + 1])
        if not (left_ok and right_ok):
            print(f"  FAIL find_peak_element {nums} -> idx={idx} not a peak")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} find_peak_element")

    # find_min_rotated
    cases = [
        ([3, 4, 5, 1, 2], 1),
        ([4, 5, 6, 7, 0, 1, 2], 0),
        ([11, 13, 15, 17], 11),
        ([2, 1], 1),
        ([1], 1),
    ]
    ok = True
    for nums, exp in cases:
        res = find_min_rotated(nums)
        if res != exp:
            print(f"  FAIL find_min_rotated {nums} -> {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} find_min_rotated")

    # search_2d_matrix
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    cases = [(3, True), (13, False), (1, True), (60, True), (0, False)]
    ok = True
    for tgt, exp in cases:
        res = search_2d_matrix(matrix, tgt)
        if res != exp:
            print(f"  FAIL search_2d_matrix target={tgt} -> {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} search_2d_matrix")

    # sqrt_binary_search
    cases = [(0, 0), (1, 1), (2, 1), (4, 2), (8, 2), (9, 3), (15, 3), (16, 4)]
    ok = True
    for x, exp in cases:
        res = sqrt_binary_search(x)
        if res != exp:
            print(f"  FAIL sqrt_binary_search {x} -> {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} sqrt_binary_search")

    # ship_within_days
    cases = [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 15),
        ([3, 2, 2, 4, 1, 4], 3, 6),
        ([1, 2, 3, 1, 1], 4, 3),
    ]
    ok = True
    for w, d, exp in cases:
        res = ship_within_days(w, d)
        if res != exp:
            print(f"  FAIL ship_within_days {w}, days={d} -> {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} ship_within_days")

    # split_array_largest_sum
    cases = [
        ([7, 2, 5, 10, 8], 2, 18),
        ([1, 2, 3, 4, 5], 2, 9),
        ([1, 4, 4], 3, 4),
    ]
    ok = True
    for nums, m, exp in cases:
        res = split_array_largest_sum(nums, m)
        if res != exp:
            print(f"  FAIL split_array_largest_sum {nums}, m={m} -> {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} split_array_largest_sum")

    print("\nAll binary search application tests completed!")
