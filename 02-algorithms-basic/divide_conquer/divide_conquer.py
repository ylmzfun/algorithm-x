"""
Classic Divide & Conquer Algorithms
====================================

Divide-and-conquer solves problems by:
  1. Divide   — break the problem into smaller sub-problems.
  2. Conquer  — solve each sub-problem recursively.
  3. Combine  — merge sub-solutions into a global solution.

Functions:
- binary_search_dc    : Binary search as a divide & conquer routine.
- merge_sort_dc       : Merge sort (recursive, stable).
- quick_sort_dc       : Quick sort (random pivot).
- find_max_min_dc     : Find max and min simultaneously with ~3n/2 comparisons.
- closest_pair        : Closest pair of points in 2D (O(n log n)).
- count_inversions    : Count inversions in an array via modified merge sort.
"""

import math
import random
from typing import List, Tuple, Optional


# ---------------------------------------------------------------------------
# Binary Search as Divide & Conquer
# ---------------------------------------------------------------------------

def binary_search_dc(arr: List[int], target: int, lo: int = 0,
                     hi: Optional[int] = None) -> int:
    """
    Binary search expressed as a recursive divide-and-conquer routine.

    Parameters
    ----------
    arr : List[int]
        Sorted ascending list.
    target : int
        Value to find.
    lo, hi : int
        Search range (inclusive).

    Returns
    -------
    int
        Index of target, or -1.

    Time  : O(log n)
    Space : O(log n) recursion
    """
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = lo + (hi - lo) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_dc(arr, target, mid + 1, hi)
    else:
        return binary_search_dc(arr, target, lo, mid - 1)


# ---------------------------------------------------------------------------
# Merge Sort as Divide & Conquer
# ---------------------------------------------------------------------------

def _merge(arr: List[int], aux: List[int], lo: int, mid: int, hi: int) -> None:
    for k in range(lo, hi + 1):
        aux[k] = arr[k]
    i, j = lo, mid + 1
    for k in range(lo, hi + 1):
        if i > mid:
            arr[k] = aux[j]; j += 1
        elif j > hi:
            arr[k] = aux[i]; i += 1
        elif aux[i] <= aux[j]:
            arr[k] = aux[i]; i += 1
        else:
            arr[k] = aux[j]; j += 1


def _merge_sort(arr: List[int], aux: List[int], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    mid = (lo + hi) // 2
    _merge_sort(arr, aux, lo, mid)
    _merge_sort(arr, aux, mid + 1, hi)
    _merge(arr, aux, lo, mid, hi)


def merge_sort_dc(arr: List[int]) -> List[int]:
    """
    Sort using merge sort — a canonical divide & conquer algorithm.

    Time  : O(n log n)
    Space : O(n)
    """
    a = arr[:]
    aux = [0] * len(a)
    _merge_sort(a, aux, 0, len(a) - 1)
    return a


# ---------------------------------------------------------------------------
# Quick Sort as Divide & Conquer
# ---------------------------------------------------------------------------

def _partition(arr: List[int], lo: int, hi: int) -> int:
    pi = random.randint(lo, hi)
    arr[pi], arr[hi] = arr[hi], arr[pi]
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i


def _quick_sort(arr: List[int], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    p = _partition(arr, lo, hi)
    _quick_sort(arr, lo, p - 1)
    _quick_sort(arr, p + 1, hi)


def quick_sort_dc(arr: List[int]) -> List[int]:
    """
    Sort using quick sort with random pivot — divide & conquer.

    Time  : O(n log n) average
    Space : O(log n) recursion
    """
    a = arr[:]
    _quick_sort(a, 0, len(a) - 1)
    return a


# ---------------------------------------------------------------------------
# Find Max and Min Simultaneously (fewer comparisons)
# ---------------------------------------------------------------------------

def find_max_min_dc(arr: List[int]) -> Tuple[int, int]:
    """
    Find the maximum and minimum of an array simultaneously using divide &
    conquer, requiring approximately 3n/2 - 2 comparisons.

    Parameters
    ----------
    arr : List[int]
        Non-empty list.

    Returns
    -------
    Tuple[int, int]
        (minimum, maximum).

    Time  : O(n) with ~1.5n comparisons.
    Space : O(log n) recursion.
    """
    n = len(arr)

    def _dc(lo: int, hi: int) -> Tuple[int, int]:
        if lo == hi:
            return arr[lo], arr[lo]
        if hi == lo + 1:
            return (arr[lo], arr[hi]) if arr[lo] < arr[hi] else (arr[hi], arr[lo])
        mid = (lo + hi) // 2
        min1, max1 = _dc(lo, mid)
        min2, max2 = _dc(mid + 1, hi)
        return min(min1, min2), max(max1, max2)

    return _dc(0, n - 1)


# ---------------------------------------------------------------------------
# Closest Pair of Points (2D)
# ---------------------------------------------------------------------------

Point = Tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def _closest_strip(strip: List[Point], d: float) -> float:
    """Check points in the central strip; strip is sorted by y."""
    min_d = d
    n = len(strip)
    for i in range(n):
        j = i + 1
        while j < n and (strip[j][1] - strip[i][1]) < min_d:
            min_d = min(min_d, _dist(strip[i], strip[j]))
            j += 1
    return min_d


def _closest_rec(px: List[Point], py: List[Point]) -> float:
    n = len(px)
    if n <= 3:
        # Brute force
        min_d = float("inf")
        for i in range(n):
            for j in range(i + 1, n):
                min_d = min(min_d, _dist(px[i], px[j]))
        return min_d

    mid = n // 2
    mid_x = px[mid][0]

    # Divide py into left and right, preserving y-order
    pyl = [p for p in py if p[0] <= mid_x]
    pyr = [p for p in py if p[0] > mid_x]

    dl = _closest_rec(px[:mid], pyl)
    dr = _closest_rec(px[mid:], pyr)
    d = min(dl, dr)

    # Build strip of points within d of the midline
    strip = [p for p in py if abs(p[0] - mid_x) < d]
    return min(d, _closest_strip(strip, d))


def closest_pair(points: List[Point]) -> float:
    """
    Find the closest pair distance among a set of 2D points in O(n log n).

    Parameters
    ----------
    points : List[Tuple[float, float]]
        List of (x, y) coordinates.

    Returns
    -------
    float
        Distance between the two closest points.

    Time  : O(n log n)
    Space : O(n)

    Raises
    ------
    ValueError
        If fewer than 2 points are provided.
    """
    if len(points) < 2:
        raise ValueError("Need at least 2 points")
    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    return _closest_rec(px, py)


# ---------------------------------------------------------------------------
# Count Inversions
# ---------------------------------------------------------------------------

def _count_inv_merge(arr: List[int], aux: List[int], lo: int, mid: int,
                     hi: int) -> int:
    """Merge and count inversions."""
    for k in range(lo, hi + 1):
        aux[k] = arr[k]
    i, j, inv = lo, mid + 1, 0
    for k in range(lo, hi + 1):
        if i > mid:
            arr[k] = aux[j]; j += 1
        elif j > hi:
            arr[k] = aux[i]; i += 1
        elif aux[i] <= aux[j]:
            arr[k] = aux[i]; i += 1
        else:
            arr[k] = aux[j]; j += 1
            inv += (mid - i + 1)  # all remaining left-side > aux[j]
    return inv


def _count_inv_rec(arr: List[int], aux: List[int], lo: int, hi: int) -> int:
    if lo >= hi:
        return 0
    mid = (lo + hi) // 2
    inv = _count_inv_rec(arr, aux, lo, mid)
    inv += _count_inv_rec(arr, aux, mid + 1, hi)
    inv += _count_inv_merge(arr, aux, lo, mid, hi)
    return inv


def count_inversions(arr: List[int]) -> int:
    """
    Count the number of inversions in an array.  An inversion is a pair
    (i, j) such that i < j and arr[i] > arr[j].

    Uses a modified merge sort (divide & conquer).

    Parameters
    ----------
    arr : List[int]
        Input array.

    Returns
    -------
    int
        Number of inversions.

    Time  : O(n log n)
    Space : O(n)

    Example
    -------
    >>> count_inversions([2, 4, 1, 3, 5])
    3   # (2,1), (4,1), (4,3)
    """
    a = arr[:]
    aux = [0] * len(a)
    return _count_inv_rec(a, aux, 0, len(a) - 1)


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Divide & Conquer Tests ===\n")

    # binary_search_dc
    arr = [1, 3, 5, 7, 9, 11]
    ok = all(binary_search_dc(arr, x) == i for i, x in enumerate(arr))
    ok = ok and binary_search_dc(arr, 4) == -1
    print(f"  {'PASS' if ok else 'FAIL'} binary_search_dc")

    # merge_sort_dc
    ok = merge_sort_dc([5, 2, 8, 1, 9, 3]) == [1, 2, 3, 5, 8, 9]
    ok = ok and merge_sort_dc([]) == []
    print(f"  {'PASS' if ok else 'FAIL'} merge_sort_dc")

    # quick_sort_dc
    ok = quick_sort_dc([5, 2, 8, 1, 9, 3]) == [1, 2, 3, 5, 8, 9]
    ok = ok and quick_sort_dc([]) == []
    print(f"  {'PASS' if ok else 'FAIL'} quick_sort_dc")

    # find_max_min_dc
    for arr in ([3, 1, 4, 1, 5, 9, 2], [5], [2, 7], [-5, 0, 3, -2]):
        mn, mx = find_max_min_dc(arr)
        assert mn == min(arr) and mx == max(arr), f"Failed on {arr}"
    print("  PASS find_max_min_dc")

    # closest_pair
    pts1: List[Point] = [(0, 0), (1, 1), (2, 2), (0.5, 0.5)]
    d1 = closest_pair(pts1)
    assert abs(d1 - math.hypot(0.5, 0.5)) < 1e-9, f"closest_pair failed: {d1}"

    pts2: List[Point] = [(0, 0), (3, 4), (6, 8)]
    d2 = closest_pair(pts2)
    assert abs(d2 - 5.0) < 1e-9, f"closest_pair (5) failed: {d2}"
    print("  PASS closest_pair")

    # count_inversions
    cases = [
        ([1, 2, 3, 4, 5], 0),
        ([5, 4, 3, 2, 1], 10),
        ([2, 4, 1, 3, 5], 3),
        ([1, 3, 5, 2, 4, 6], 3),
        ([], 0),
    ]
    ok = True
    for arr, exp in cases:
        res = count_inversions(arr)
        if res != exp:
            print(f"  FAIL count_inversions {arr} -> {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} count_inversions")

    print("\nAll divide & conquer tests completed!")
