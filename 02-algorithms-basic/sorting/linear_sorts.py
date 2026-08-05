"""
Linear-Time (Non-Comparison) Sorting Algorithms
================================================

These sorts achieve O(n) time by exploiting constraints on the input domain
rather than comparing elements.

- counting_sort : O(n + k) — for integer keys in a known small range [0, k).
- bucket_sort   : O(n + k) average — distributes elements into buckets,
                   then sorts each bucket (typically with insertion sort).
- radix_sort_lsd: O(d·(n + b)) — least-significant-digit-first radix sort
                   using counting sort as a stable sub-routine.
"""

from typing import List


# ---------------------------------------------------------------------------
# Counting Sort
# ---------------------------------------------------------------------------

def counting_sort(arr: List[int]) -> List[int]:
    """
    Sort a list of non-negative integers using counting sort.

    Works by counting the frequency of each distinct value, then computing
    cumulative counts to determine each element's final position.

    Parameters
    ----------
    arr : List[int]
        List of non-negative integers.

    Returns
    -------
    List[int]
        A new sorted list.

    Time  : O(n + k), where k = max(arr).
    Space : O(n + k).
    Stable: yes.

    Raises
    ------
    ValueError
        If any element is negative.
    """
    if not arr:
        return []

    if any(x < 0 for x in arr):
        raise ValueError("counting_sort requires non-negative integers")

    max_val = max(arr)
    count = [0] * (max_val + 1)

    for x in arr:
        count[x] += 1

    # Cumulative counts
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    output: List[int] = [0] * len(arr)
    # Traverse backwards for stability
    for x in reversed(arr):
        count[x] -= 1
        output[count[x]] = x

    return output


# ---------------------------------------------------------------------------
# Bucket Sort
# ---------------------------------------------------------------------------

def _insertion_sort_float(bucket: List[float]) -> None:
    """In-place insertion sort for a small bucket of floats."""
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key


def bucket_sort(arr: List[float], num_buckets: int = 10) -> List[float]:
    """
    Sort a list of floats uniformly distributed in [0, 1) using bucket sort.

    Each element is placed into one of `num_buckets` equally-sized buckets;
    each bucket is sorted individually (insertion sort), then concatenated.

    Parameters
    ----------
    arr : List[float]
        List of floats in [0, 1).
    num_buckets : int
        Number of buckets to use (default 10).

    Returns
    -------
    List[float]
        A new sorted list.

    Time  : O(n + k) average; O(n²) worst if many elements fall into one
            bucket.
    Space : O(n + k).

    Raises
    ------
    ValueError
        If any element is outside [0, 1).
    """
    if not arr:
        return []

    if any(not (0.0 <= x < 1.0) for x in arr):
        raise ValueError("bucket_sort expects floats in [0, 1)")

    buckets: List[List[float]] = [[] for _ in range(num_buckets)]

    for x in arr:
        idx = min(int(x * num_buckets), num_buckets - 1)
        buckets[idx].append(x)

    result: List[float] = []
    for bucket in buckets:
        _insertion_sort_float(bucket)
        result.extend(bucket)

    return result


# ---------------------------------------------------------------------------
# Radix Sort (LSD)
# ---------------------------------------------------------------------------

def _counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
    """
    Perform a stable counting sort on arr based on the digit at position exp.
    exp = 1, 10, 100, … (base 10).
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for x in arr:
        digit = (x // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for x in reversed(arr):
        digit = (x // exp) % 10
        count[digit] -= 1
        output[count[digit]] = x

    return output


def radix_sort_lsd(arr: List[int]) -> List[int]:
    """
    Sort a list of non-negative integers using LSD (Least Significant Digit)
    radix sort with base 10.

    Sorts digit by digit, starting from the least significant digit, using a
    stable counting sort as the subroutine.

    Parameters
    ----------
    arr : List[int]
        List of non-negative integers.

    Returns
    -------
    List[int]
        A new sorted list.

    Time  : O(d·n) where d is the number of digits in the maximum element.
    Space : O(n).
    Stable: yes.

    Raises
    ------
    ValueError
        If any element is negative.
    """
    if not arr:
        return []

    if any(x < 0 for x in arr):
        raise ValueError("radix_sort_lsd requires non-negative integers")

    max_val = max(arr)
    result = arr[:]
    exp = 1
    while max_val // exp > 0:
        result = _counting_sort_by_digit(result, exp)
        exp *= 10
    return result


# ===========================================================================
# Tests
# ===========================================================================

def _test(name: str, func, cases) -> bool:
    all_pass = True
    for arr, expected in cases:
        result = func(arr)
        if result != expected:
            print(f"  FAIL {name}: {arr} -> {result}, expected {expected}")
            all_pass = False
    if all_pass:
        print(f"  PASS {name}")
    return all_pass


if __name__ == "__main__":
    print("=== Linear Sorting Tests ===\n")

    # Counting sort
    _test("counting_sort", counting_sort, [
        ([4, 2, 2, 8, 3, 3, 1], [1, 2, 2, 3, 3, 4, 8]),
        ([0, 0, 0], [0, 0, 0]),
        ([5], [5]),
        ([], []),
        ([9, 1, 5, 3, 7], [1, 3, 5, 7, 9]),
    ])
    try:
        counting_sort([-1, 2])
        print("  FAIL counting_sort: should raise ValueError for negatives")
    except ValueError:
        print("  PASS counting_sort: raises ValueError for negatives")

    # Bucket sort
    _test("bucket_sort", bucket_sort, [
        ([0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51],
         [0.32, 0.33, 0.37, 0.42, 0.47, 0.51, 0.52]),
        ([0.1], [0.1]),
        ([], []),
        ([0.0, 0.99, 0.5, 0.25, 0.75], [0.0, 0.25, 0.5, 0.75, 0.99]),
    ])
    try:
        bucket_sort([1.5])
        print("  FAIL bucket_sort: should raise ValueError for out-of-range")
    except ValueError:
        print("  PASS bucket_sort: raises ValueError for out-of-range")

    # Radix sort
    _test("radix_sort_lsd", radix_sort_lsd, [
        ([170, 45, 75, 90, 802, 24, 2, 66],
         [2, 24, 45, 66, 75, 90, 170, 802]),
        ([3, 1, 4, 1, 5, 9, 2, 6], [1, 1, 2, 3, 4, 5, 6, 9]),
        ([100, 10, 1], [1, 10, 100]),
        ([0], [0]),
        ([], []),
    ])
    try:
        radix_sort_lsd([-5, 3])
        print("  FAIL radix_sort_lsd: should raise ValueError for negatives")
    except ValueError:
        print("  PASS radix_sort_lsd: raises ValueError for negatives")

    # Large random test
    print("\n--- Large random array test ---")
    import random
    for _ in range(3):
        large = [random.randint(0, 10000) for _ in range(1000)]
        assert counting_sort(large) == sorted(large)
        assert radix_sort_lsd(large) == sorted(large)
    print("  PASS counting_sort & radix_sort_lsd on 3×1000 random arrays")

    floats = [random.random() for _ in range(500)]
    result = bucket_sort(floats)
    assert result == sorted(floats), "Bucket sort failed"
    print("  PASS bucket_sort on 500 random floats")
