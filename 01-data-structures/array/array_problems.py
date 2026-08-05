"""
Common Array Problems and Solutions
====================================

This module contains classical array-based algorithmic problems with
well-documented solutions including time/space complexity analysis.

Problems covered:
    1. Two Sum — Find two numbers that add up to a target.
    2. Maximum Subarray (Kadane's algorithm) — Largest contiguous sum.
    3. Rotate Array — Rotate elements by k positions.
    4. Merge Intervals — Merge overlapping intervals.
    5. Product Except Self — Product of all elements except current.
    6. Find Duplicate — Find the duplicate number (Floyd's cycle detection).
    7. Missing Number — Find the missing number in range [0, n].
"""

from typing import List, Optional, Tuple


# ─── 1. Two Sum ────────────────────────────────────────────────────────────────


def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Find indices of two numbers that add up to `target`.

    Uses a hash map to track seen values and their indices for O(n) lookup.

    Args:
        nums: List of integers.
        target: The target sum.

    Returns:
        A tuple of two indices (i, j) such that nums[i] + nums[j] == target,
        or None if no such pair exists.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Examples:
        >>> two_sum([2, 7, 11, 15], 9)
        (0, 1)
        >>> two_sum([3, 2, 4], 6)
        (1, 2)
    """
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


# ─── 2. Maximum Subarray (Kadane's Algorithm) ─────────────────────────────────


def max_subarray(nums: List[int]) -> Tuple[int, int, int]:
    """Find the contiguous subarray with the largest sum (Kadane's algorithm).

    Args:
        nums: List of integers (may contain negative numbers).

    Returns:
        A tuple (max_sum, start_index, end_index) where end_index is inclusive.
        Returns (0, 0, -1) for empty input.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Examples:
        >>> max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
        (6, 3, 6)
        >>> max_subarray([1])
        (1, 0, 0)
        >>> max_subarray([5, 4, -1, 7, 8])
        (23, 0, 4)
    """
    if not nums:
        return (0, 0, -1)

    max_sum = nums[0]
    current_sum = nums[0]
    max_start = max_end = 0
    current_start = 0

    for i in range(1, len(nums)):
        if current_sum < 0:
            # Start a new subarray
            current_sum = nums[i]
            current_start = i
        else:
            # Extend current subarray
            current_sum += nums[i]

        if current_sum > max_sum:
            max_sum = current_sum
            max_start = current_start
            max_end = i

    return (max_sum, max_start, max_end)


# ─── 3. Rotate Array ──────────────────────────────────────────────────────────


def rotate_array(nums: List[int], k: int) -> None:
    """Rotate array to the right by k steps (in-place).

    Uses the three-reverse technique: reverse whole, reverse first k, reverse rest.

    Args:
        nums: List to rotate (modified in-place).
        k: Number of positions to rotate right.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Examples:
        >>> arr = [1, 2, 3, 4, 5, 6, 7]
        >>> rotate_array(arr, 3)
        >>> arr
        [5, 6, 7, 1, 2, 3, 4]
    """

    def reverse(start: int, end: int) -> None:
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    n = len(nums)
    if n == 0:
        return
    k %= n
    if k == 0:
        return

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)


# ─── 4. Merge Intervals ───────────────────────────────────────────────────────


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Merge all overlapping intervals.

    Sorts intervals by start time, then merges overlapping ones linearly.

    Args:
        intervals: List of intervals where each interval is [start, end].

    Returns:
        A new list of non-overlapping intervals covering the same ranges.

    Time Complexity: O(n log n) — dominated by sorting.
    Space Complexity: O(n) — for output list.

    Examples:
        >>> merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
        [[1, 6], [8, 10], [15, 18]]
        >>> merge_intervals([[1, 4], [4, 5]])
        [[1, 5]]
    """
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    merged: List[List[int]] = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            # Overlapping — merge
            last[1] = max(last[1], current[1])
        else:
            # No overlap — add new interval
            merged.append(current)

    return merged


# ─── 5. Product Except Self ───────────────────────────────────────────────────


def product_except_self(nums: List[int]) -> List[int]:
    """Return an array where output[i] = product of all elements except nums[i].

    Computes in O(n) without using division, using two passes:
    one for prefix products and one for suffix products.

    Args:
        nums: List of integers.

    Returns:
        List where each element is the product of all elements except the one
        at that index.

    Time Complexity: O(n)
    Space Complexity: O(1) — output array not counted as extra space.

    Examples:
        >>> product_except_self([1, 2, 3, 4])
        [24, 12, 8, 6]
        >>> product_except_self([-1, 1, 0, -3, 3])
        [0, 0, 9, 0, 0]
    """
    n = len(nums)
    result = [1] * n

    # Prefix products (left to right)
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Suffix products (right to left) — multiply into result
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result


# ─── 6. Find Duplicate ───────────────────────────────────────────────────────


def find_duplicate(nums: List[int]) -> int:
    """Find the duplicate number using Floyd's cycle detection (tortoise & hare).

    Given an array of n+1 integers where each is in [1, n] and exactly one
    number is duplicated (possibly multiple times), find the duplicate.

    Treats the array as a linked list where nums[i] is the "next" pointer.
    Because of the pigeonhole principle, a cycle must exist.

    Args:
        nums: List of length n+1 with values in [1, n], one duplicate.

    Returns:
        The duplicate number.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Examples:
        >>> find_duplicate([1, 3, 4, 2, 2])
        2
        >>> find_duplicate([3, 1, 3, 4, 2])
        3
    """
    # Phase 1: Detect cycle
    slow = nums[0]
    fast = nums[0]

    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find cycle entry point (the duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow


# ─── 7. Missing Number ────────────────────────────────────────────────────────


def missing_number(nums: List[int]) -> int:
    """Find the missing number in range [0, n] where n = len(nums).

    Uses XOR trick: XOR of all indices and values. Every number that appears
    twice cancels out, leaving the missing one.

    Args:
        nums: List containing n distinct numbers from [0, n] except one missing.

    Returns:
        The missing number.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Examples:
        >>> missing_number([3, 0, 1])
        2
        >>> missing_number([0, 1])
        2
        >>> missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1])
        8
    """
    n = len(nums)
    result = n  # Start with n (the index that doesn't appear as array index)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result


# ─── Helper: all_pairs_two_sum ───────────────────────────────────────────────


def two_sum_all_pairs(nums: List[int], target: int) -> List[Tuple[int, int]]:
    """Return all unique index pairs that sum to target.

    Args:
        nums: List of integers.
        target: The target sum.

    Returns:
        List of (i, j) tuples with i < j and nums[i] + nums[j] == target.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen: dict[int, List[int]] = {}
    result: List[Tuple[int, int]] = []

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            for j in seen[complement]:
                result.append((j, i))
        seen.setdefault(num, []).append(i)

    return result


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_tests() -> None:
    """Run all tests and report results."""
    import sys

    passed = 0
    failed = 0

    def check(description: str, condition: bool) -> None:
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  ✓ {description}")
        else:
            failed += 1
            print(f"  ✗ {description}", file=sys.stderr)

    # ── Two Sum ────────────────────────────────────────────────────────────────
    print("Two Sum:")
    check("basic case", two_sum([2, 7, 11, 15], 9) == (0, 1))
    check("unordered", two_sum([3, 2, 4], 6) == (1, 2))
    check("duplicates", two_sum([3, 3], 6) == (0, 1))
    check("no solution", two_sum([1, 2, 3], 10) is None)
    check("empty list", two_sum([], 5) is None)
    check("all pairs", sorted(two_sum_all_pairs([1, 2, 3, 4, 4], 5)) == [(0, 3), (0, 4), (1, 2)])

    # ── Max Subarray ───────────────────────────────────────────────────────────
    print("\nMax Subarray (Kadane):")
    check("classic case", max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == (6, 3, 6))
    check("single element", max_subarray([1]) == (1, 0, 0))
    check("all positive", max_subarray([5, 4, -1, 7, 8]) == (23, 0, 4))
    check("all negative", max_subarray([-1, -2, -3]) == (-1, 0, 0))
    check("empty", max_subarray([]) == (0, 0, -1))

    # ── Rotate Array ───────────────────────────────────────────────────────────
    print("\nRotate Array:")
    arr1 = [1, 2, 3, 4, 5, 6, 7]
    rotate_array(arr1, 3)
    check("k=3 on 7 elements", arr1 == [5, 6, 7, 1, 2, 3, 4])

    arr2 = [-1, -100, 3, 99]
    rotate_array(arr2, 2)
    check("with negatives", arr2 == [3, 99, -1, -100])

    arr3 = [1, 2, 3]
    rotate_array(arr3, 0)
    check("k=0 no change", arr3 == [1, 2, 3])

    arr4 = [1, 2, 3]
    rotate_array(arr4, 3)
    check("k==n no change", arr4 == [1, 2, 3])

    arr5 = [1, 2, 3]
    rotate_array(arr5, 5)  # k % n = 2
    check("k>n", arr5 == [2, 3, 1])

    arr6: List[int] = []
    rotate_array(arr6, 5)
    check("empty array", arr6 == [])

    # ── Merge Intervals ────────────────────────────────────────────────────────
    print("\nMerge Intervals:")
    check("overlapping", merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) ==
          [[1, 6], [8, 10], [15, 18]])
    check("adjacent", merge_intervals([[1, 4], [4, 5]]) == [[1, 5]])
    check("no overlap", merge_intervals([[1, 2], [3, 4]]) == [[1, 2], [3, 4]])
    check("nested", merge_intervals([[1, 10], [2, 3], [4, 5]]) == [[1, 10]])
    check("empty", merge_intervals([]) == [])
    check("single", merge_intervals([[1, 5]]) == [[1, 5]])

    # ── Product Except Self ────────────────────────────────────────────────────
    print("\nProduct Except Self:")
    check("basic", product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6])
    check("with zero", product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0])
    check("two elements", product_except_self([2, 3]) == [3, 2])
    check("all ones", product_except_self([1, 1, 1]) == [1, 1, 1])

    # ── Find Duplicate ─────────────────────────────────────────────────────────
    print("\nFind Duplicate:")
    check("basic", find_duplicate([1, 3, 4, 2, 2]) == 2)
    check("start duplicate", find_duplicate([3, 1, 3, 4, 2]) == 3)
    check("adjacent duplicate", find_duplicate([1, 1]) == 1)
    check("larger case", find_duplicate([2, 5, 9, 6, 9, 3, 8, 9, 7, 1]) == 9)

    # ── Missing Number ─────────────────────────────────────────────────────────
    print("\nMissing Number:")
    check("basic", missing_number([3, 0, 1]) == 2)
    check("missing last", missing_number([0, 1]) == 2)
    check("missing first", missing_number([1, 2]) == 0)
    check("larger case", missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8)
    check("single element [0]", missing_number([0]) == 1)

    # ── Summary ────────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
