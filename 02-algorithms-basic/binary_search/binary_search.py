"""
Core Binary Search Functions
=============================

All implementations are iterative (no recursion) to avoid stack overflow and
to make them easy to reason about.

Functions:
- binary_search                  : Standard search for any occurrence.
- binary_search_first_occurrence : Leftmost index matching target.
- binary_search_last_occurrence  : Rightmost index matching target.
- binary_search_first_ge         : First index with value >= target (lower_bound).
- binary_search_last_le          : Last index with value <= target (upper_bound-like).
"""

from typing import List, Optional, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Standard Binary Search
# ---------------------------------------------------------------------------

def binary_search(arr: List[T], target: T) -> int:
    """
    Perform standard binary search on a sorted list.

    Parameters
    ----------
    arr : List[T]
        Sorted (ascending) list to search.
    target : T
        Value to find.

    Returns
    -------
    int
        Index of ``target`` if found, otherwise -1.

    Time  : O(log n)
    Space : O(1)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ---------------------------------------------------------------------------
# First Occurrence (leftmost)
# ---------------------------------------------------------------------------

def binary_search_first_occurrence(arr: List[T], target: T) -> int:
    """
    Find the index of the **first** occurrence of ``target``.

    Parameters
    ----------
    arr : List[T]
        Sorted (ascending) list, possibly containing duplicates.
    target : T
        Value to find.

    Returns
    -------
    int
        Leftmost index of ``target``, or -1 if not present.

    Time  : O(log n)
    Space : O(1)
    """
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            result = mid
            hi = mid - 1  # keep searching left
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


# ---------------------------------------------------------------------------
# Last Occurrence (rightmost)
# ---------------------------------------------------------------------------

def binary_search_last_occurrence(arr: List[T], target: T) -> int:
    """
    Find the index of the **last** occurrence of ``target``.

    Parameters
    ----------
    arr : List[T]
        Sorted (ascending) list, possibly containing duplicates.
    target : T
        Value to find.

    Returns
    -------
    int
        Rightmost index of ``target``, or -1 if not present.

    Time  : O(log n)
    Space : O(1)
    """
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            result = mid
            lo = mid + 1  # keep searching right
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


# ---------------------------------------------------------------------------
# First >= target  (lower_bound)
# ---------------------------------------------------------------------------

def binary_search_first_ge(arr: List[T], target: T) -> int:
    """
    Find the index of the **first** element >= ``target`` (lower_bound).

    Parameters
    ----------
    arr : List[T]
        Sorted (ascending) list.
    target : T
        Threshold value.

    Returns
    -------
    int
        Index of first element >= ``target``, or ``len(arr)`` if all are
        smaller.

    Time  : O(log n)
    Space : O(1)
    """
    lo, hi = 0, len(arr) - 1
    result = len(arr)
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] >= target:
            result = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return result


# ---------------------------------------------------------------------------
# Last <= target  (floor / upper_bound-like)
# ---------------------------------------------------------------------------

def binary_search_last_le(arr: List[T], target: T) -> int:
    """
    Find the index of the **last** element <= ``target``.

    Parameters
    ----------
    arr : List[T]
        Sorted (ascending) list.
    target : T
        Threshold value.

    Returns
    -------
    int
        Index of last element <= ``target``, or -1 if all are larger.

    Time  : O(log n)
    Space : O(1)
    """
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:
            result = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return result


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Binary Search Tests ===\n")

    arr = [1, 2, 3, 3, 3, 5, 7, 9, 9, 11]

    tests: List[bool] = []

    # binary_search
    cases = [(3, True), (5, True), (1, True), (11, True), (4, False), (0, False), (12, False)]
    for tgt, should_find in cases:
        idx = binary_search(arr, tgt)
        ok = (idx != -1) == should_find
        if not ok:
            print(f"  FAIL binary_search target={tgt}: idx={idx}, should_find={should_find}")
        tests.append(ok)
    print(f"  {'PASS' if all(tests) else 'FAIL'} binary_search (basic)")

    # first_occurrence
    tests = []
    cases = [(3, 2), (9, 7), (1, 0), (11, 9), (4, -1)]
    for tgt, expected in cases:
        idx = binary_search_first_occurrence(arr, tgt)
        ok = idx == expected
        if not ok:
            print(f"  FAIL first_occurrence target={tgt}: {idx} != {expected}")
        tests.append(ok)
    print(f"  {'PASS' if all(tests) else 'FAIL'} binary_search_first_occurrence")

    # last_occurrence
    tests = []
    cases = [(3, 4), (9, 8), (1, 0), (11, 9), (4, -1)]
    for tgt, expected in cases:
        idx = binary_search_last_occurrence(arr, tgt)
        ok = idx == expected
        if not ok:
            print(f"  FAIL last_occurrence target={tgt}: {idx} != {expected}")
        tests.append(ok)
    print(f"  {'PASS' if all(tests) else 'FAIL'} binary_search_last_occurrence")

    # first_ge
    tests = []
    cases = [(3, 2), (4, 5), (0, 0), (12, 10), (10, 9)]
    for tgt, expected in cases:
        idx = binary_search_first_ge(arr, tgt)
        ok = idx == expected
        if not ok:
            print(f"  FAIL first_ge target={tgt}: {idx} != {expected}")
        tests.append(ok)
    print(f"  {'PASS' if all(tests) else 'FAIL'} binary_search_first_ge")

    # last_le
    tests = []
    cases = [(3, 4), (4, 4), (0, -1), (12, 9), (10, 8)]
    for tgt, expected in cases:
        idx = binary_search_last_le(arr, tgt)
        ok = idx == expected
        if not ok:
            print(f"  FAIL last_le target={tgt}: {idx} != {expected}")
        tests.append(ok)
    print(f"  {'PASS' if all(tests) else 'FAIL'} binary_search_last_le")

    # Edge cases
    print("\n--- Edge cases ---")
    for func, name in [
        (binary_search, "binary_search"),
        (binary_search_first_occurrence, "first_occurrence"),
        (binary_search_last_occurrence, "last_occurrence"),
    ]:
        assert func([], 5) == -1, f"{name} on empty array"
        assert func([1], 1) in (0,), f"{name} single element found"
        assert func([1], 2) == -1, f"{name} single element not found"
    assert binary_search_first_ge([], 5) == 0
    assert binary_search_last_le([], 5) == -1
    print("  PASS edge cases")

    print("\nAll binary search tests completed!")
