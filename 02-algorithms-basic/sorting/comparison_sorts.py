"""
Comparison-Based Sorting Algorithms
====================================

This module implements classic comparison-based sorting algorithms, ranging
from simple O(n²) quadratic sorts to efficient O(n log n) divide-and-conquer
and heap-based sorts.

Algorithms implemented:
- bubble_sort       : O(n²) average/worst, O(n) best (with early exit)
- selection_sort    : O(n²) always, minimal swaps
- insertion_sort    : O(n²) average/worst, O(n) best, stable, adaptive
- shell_sort        : O(n^(3/2)) with Hibbard gap sequence
- merge_sort        : O(n log n) stable, recursive top-down
- merge_sort_iterative : O(n log n) bottom-up iterative merge
- merge_sort_bottom_up : O(n log n) bottom-up (alias)
- quick_sort        : O(n log n) average, O(n²) worst, in-place,
                      random pivot
- quick_sort_three_way : O(n log n) average, handles duplicates
                         efficiently via three-way partitioning
- heap_sort         : O(n log n) worst-case, in-place, not stable
"""

import random
from typing import List, TypeVar, Optional

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Bubble Sort
# ---------------------------------------------------------------------------

def bubble_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using bubble sort.

    Repeatedly steps through the list, compares adjacent elements, and swaps
    them if they are in the wrong order.  An early-exit optimisation stops
    early when no swaps occur in a full pass.

    Parameters
    ----------
    arr : List[T]
        The list to sort (not modified in place; returns a new list).

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n²) worst/average, O(n) best (already sorted).
    Space : O(n) for the copy (or O(1) auxiliary for in-place use).
    """
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


# ---------------------------------------------------------------------------
# Selection Sort
# ---------------------------------------------------------------------------

def selection_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using selection sort.

    Repeatedly finds the minimum element from the unsorted portion and places
    it at the beginning.

    Parameters
    ----------
    arr : List[T]
        The list to sort.

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n²) always.
    Space : O(n) for the copy; O(1) auxiliary swaps.
    """
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


# ---------------------------------------------------------------------------
# Insertion Sort
# ---------------------------------------------------------------------------

def insertion_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using insertion sort.

    Builds the final sorted array one item at a time by repeatedly picking the
    next element and inserting it into the correct position within the already-
    sorted prefix.

    Parameters
    ----------
    arr : List[T]
        The list to sort.

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n²) worst/average, O(n) best (already sorted).
    Space : O(n) for the copy; O(1) auxiliary.
    Stable: yes.
    """
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# ---------------------------------------------------------------------------
# Shell Sort (Hibbard gap sequence: 2^k - 1)
# ---------------------------------------------------------------------------

def shell_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using Shell sort with the Hibbard gap sequence (2^k - 1).

    Shell sort is a generalisation of insertion sort that allows the exchange
    of items that are far apart.  The Hibbard sequence yields O(n^(3/2))
    worst-case complexity.

    Parameters
    ----------
    arr : List[T]
        The list to sort.

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n^(3/2)) with Hibbard gaps.
    Space : O(n) for the copy; O(1) auxiliary.
    """
    a = arr[:]
    n = len(a)

    # Generate Hibbard gaps <= n
    gaps: List[int] = []
    k = 1
    gap = 1
    while gap <= n:
        gaps.append(gap)
        k += 1
        gap = (1 << k) - 1  # 2^k - 1
    gaps.reverse()  # sort from largest to smallest gap

    for gap in gaps:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
    return a


# ---------------------------------------------------------------------------
# Merge Sort (recursive top-down)
# ---------------------------------------------------------------------------

def _merge(a: List[T], left: int, mid: int, right: int, aux: List[Optional[T]]) -> None:
    """Merge two sorted sub-arrays a[left:mid+1] and a[mid+1:right+1]."""
    for i in range(left, right + 1):
        aux[i] = a[i]

    i, j = left, mid + 1
    for k in range(left, right + 1):
        if i > mid:
            a[k] = aux[j]  # type: ignore[assignment]
            j += 1
        elif j > right:
            a[k] = aux[i]  # type: ignore[assignment]
            i += 1
        elif aux[i] <= aux[j]:  # type: ignore[operator]
            a[k] = aux[i]  # type: ignore[assignment]
            i += 1
        else:
            a[k] = aux[j]  # type: ignore[assignment]
            j += 1


def _merge_sort_rec(a: List[T], left: int, right: int, aux: List[Optional[T]]) -> None:
    if left >= right:
        return
    mid = (left + right) // 2
    _merge_sort_rec(a, left, mid, aux)
    _merge_sort_rec(a, mid + 1, right, aux)
    _merge(a, left, mid, right, aux)


def merge_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using recursive top-down merge sort.

    Divides the array into halves, recursively sorts each half, then merges
    the sorted halves.

    Parameters
    ----------
    arr : List[T]
        The list to sort.

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n log n) always.
    Space : O(n) auxiliary.
    Stable: yes.
    """
    a = arr[:]
    aux: List[Optional[T]] = [None] * len(a)
    _merge_sort_rec(a, 0, len(a) - 1, aux)
    return a


# ---------------------------------------------------------------------------
# Merge Sort (iterative bottom-up)
# ---------------------------------------------------------------------------

def merge_sort_iterative(arr: List[T]) -> List[T]:
    """
    Sort a list using iterative (bottom-up) merge sort.

    Merges sub-arrays of size 1, 2, 4, 8, … until the whole array is sorted.
    This avoids recursion overhead.

    Parameters
    ----------
    arr : List[T]
        The list to sort.

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n log n).
    Space : O(n) auxiliary.
    Stable: yes.
    """
    a = arr[:]
    n = len(a)
    aux: List[Optional[T]] = [None] * n
    sz = 1
    while sz < n:
        for lo in range(0, n - sz, sz * 2):
            mid = lo + sz - 1
            hi = min(lo + sz * 2 - 1, n - 1)
            _merge(a, lo, mid, hi, aux)
        sz *= 2
    return a


def merge_sort_bottom_up(arr: List[T]) -> List[T]:
    """Alias for merge_sort_iterative (bottom-up merge sort)."""
    return merge_sort_iterative(arr)


# ---------------------------------------------------------------------------
# Quick Sort (random pivot)
# ---------------------------------------------------------------------------

def _quick_partition(a: List[T], lo: int, hi: int) -> int:
    """Lomuto partition scheme with random pivot."""
    pivot_idx = random.randint(lo, hi)
    a[pivot_idx], a[hi] = a[hi], a[pivot_idx]
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def _quick_sort_rec(a: List[T], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    if hi - lo < 20:
        # Use insertion sort for small sub-arrays
        for i in range(lo + 1, hi + 1):
            key = a[i]
            j = i - 1
            while j >= lo and a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = key
        return
    p = _quick_partition(a, lo, hi)
    _quick_sort_rec(a, lo, p - 1)
    _quick_sort_rec(a, p + 1, hi)


def quick_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using quick sort with random pivot selection.

    Uses the Lomuto partition scheme and switches to insertion sort for small
    sub-arrays (< 20 elements).

    Parameters
    ----------
    arr : List[T]
        The list to sort.

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n log n) average, O(n²) worst (rare with random pivot).
    Space : O(log n) for recursion stack.
    """
    a = arr[:]
    _quick_sort_rec(a, 0, len(a) - 1)
    return a


# ---------------------------------------------------------------------------
# Quick Sort (three-way partition for duplicates)
# ---------------------------------------------------------------------------

def _quick_sort_3way_rec(a: List[T], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    # 3-way partition (Dutch national flag)
    pivot_idx = random.randint(lo, hi)
    a[lo], a[pivot_idx] = a[pivot_idx], a[lo]
    pivot = a[lo]
    lt = lo
    gt = hi
    i = lo + 1
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[gt], a[i] = a[i], a[gt]
            gt -= 1
        else:
            i += 1
    _quick_sort_3way_rec(a, lo, lt - 1)
    _quick_sort_3way_rec(a, gt + 1, hi)


def quick_sort_three_way(arr: List[T]) -> List[T]:
    """
    Sort a list using three-way quick sort (Dutch national flag problem).

    Partitioning splits the array into three regions:
    < pivot, == pivot, > pivot.  This is highly efficient for arrays with
    many duplicate values (linear time in the best case).

    Parameters
    ----------
    arr : List[T]
        The list to sort.

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n log n) average, O(n) best (all equal).
    Space : O(log n) for recursion stack.
    """
    a = arr[:]
    _quick_sort_3way_rec(a, 0, len(a) - 1)
    return a


# ---------------------------------------------------------------------------
# Heap Sort
# ---------------------------------------------------------------------------

def _heapify(a: List[T], n: int, i: int) -> None:
    """Max-heapify the subtree rooted at index i."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and a[left] > a[largest]:
        largest = left
    if right < n and a[right] > a[largest]:
        largest = right

    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        _heapify(a, n, largest)


def heap_sort(arr: List[T]) -> List[T]:
    """
    Sort a list using heap sort.

    Builds a max-heap from the list, then repeatedly extracts the maximum
    element (root) and places it at the end of the array.

    Parameters
    ----------
    arr : List[T]
        The list to sort.

    Returns
    -------
    List[T]
        A new sorted list.

    Time  : O(n log n) always.
    Space : O(n) for the copy; O(1) auxiliary.
    """
    a = arr[:]
    n = len(a)

    # Build max-heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(a, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        _heapify(a, i, 0)

    return a


# ===========================================================================
# Tests
# ===========================================================================

def _test_sort(func, name: str) -> bool:
    """Test a sorting function on various cases."""
    test_cases = [
        ([64, 34, 25, 12, 22, 11, 90], [11, 12, 22, 25, 34, 64, 90]),
        ([5, 1, 4, 2, 8], [1, 2, 4, 5, 8]),
        ([1], [1]),
        ([], []),
        ([3, 3, 3, 3], [3, 3, 3, 3]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([2, 1, 2, 1, 2], [1, 1, 2, 2, 2]),
        ([-3, 9, -1, 0, 7, -5], [-5, -3, -1, 0, 7, 9]),
        (list(range(100, 0, -1)), list(range(1, 101))),
    ]
    all_pass = True
    for arr, expected in test_cases:
        result = func(arr)
        if result != expected:
            print(f"  FAIL {name}: {arr} -> {result}, expected {expected}")
            all_pass = False
    if all_pass:
        print(f"  PASS {name}")
    return all_pass


if __name__ == "__main__":
    print("=== Comparison Sorting Tests ===\n")
    tests = [
        (bubble_sort, "bubble_sort"),
        (selection_sort, "selection_sort"),
        (insertion_sort, "insertion_sort"),
        (shell_sort, "shell_sort (Hibbard)"),
        (merge_sort, "merge_sort (recursive)"),
        (merge_sort_iterative, "merge_sort (iterative)"),
        (merge_sort_bottom_up, "merge_sort_bottom_up"),
        (quick_sort, "quick_sort (random pivot)"),
        (quick_sort_three_way, "quick_sort_three_way"),
        (heap_sort, "heap_sort"),
    ]
    all_pass = True
    for func, name in tests:
        if not _test_sort(func, name):
            all_pass = False
    print(f"\n{'All tests passed!' if all_pass else 'Some tests FAILED!'}")

    # --- Large randomised stability check ---
    print("\n--- Large random array test ---")
    for _ in range(5):
        large = [random.randint(-1000, 1000) for _ in range(2000)]
        for func, name in tests:
            if func(large) != sorted(large):
                print(f"  FAIL {name} on large random array")
                break
        else:
            continue
        break
    else:
        print("  PASS all sorts on 5×2000 random arrays")
