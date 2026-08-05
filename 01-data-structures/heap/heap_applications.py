"""
Heap Applications
==================

Classic algorithmic problems solved using heaps:

1. Top K Frequent Elements — Find the K most frequent elements.
2. Kth Largest Element — Find the Kth largest element in an array.
3. Merge K Sorted Lists — Merge K sorted linked lists into one.
4. Find Median from Data Stream — Two-heap technique.
"""

import heapq
from typing import Any, List, Optional


# ─── 1. Top K Frequent Elements ───────────────────────────────────────────────


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """Return the K most frequent elements from `nums`.

    Uses a min-heap of size K to track the top elements by frequency.

    Args:
        nums: List of integers.
        k: Number of top elements to return.

    Returns:
        List of K most frequent elements (order not guaranteed).

    Time Complexity: O(n log k)
    Space Complexity: O(n) for frequency map.

    Examples:
        >>> sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2))
        [1, 2]
        >>> top_k_frequent([1], 1)
        [1]
    """
    from collections import Counter

    freq = Counter(nums)
    # Min-heap based on frequency; store as (freq, num)
    heap: List[tuple[int, int]] = []

    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for _, num in heap]


# ─── 2. Kth Largest Element ──────────────────────────────────────────────────


def kth_largest(nums: List[int], k: int) -> int:
    """Find the Kth largest element in an unsorted array.

    Uses a min-heap of size K. After processing all elements, the top of
    the heap is the Kth largest.

    Args:
        nums: List of integers.
        k: The rank (1-indexed, 1 = largest).

    Returns:
        The Kth largest element.

    Raises:
        ValueError: If k <= 0 or k > len(nums).

    Time Complexity: O(n log k)
    Space Complexity: O(k)

    Examples:
        >>> kth_largest([3, 2, 1, 5, 6, 4], 2)
        5
        >>> kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)
        4
    """
    n = len(nums)
    if k <= 0 or k > n:
        raise ValueError(f"k={k} must be in range [1, {n}]")

    min_heap: List[int] = []

    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    return min_heap[0]


def kth_smallest(nums: List[int], k: int) -> int:
    """Find the Kth smallest element using a max-heap of size K.

    Args:
        nums: List of integers.
        k: The rank (1-indexed).

    Returns:
        The Kth smallest element.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    n = len(nums)
    if k <= 0 or k > n:
        raise ValueError(f"k={k} must be in range [1, {n}]")

    # Max-heap simulated by pushing negatives
    max_heap: List[int] = []

    for num in nums:
        heapq.heappush(max_heap, -num)
        if len(max_heap) > k:
            heapq.heappop(max_heap)

    return -max_heap[0]


# ─── 3. Merge K Sorted Lists ─────────────────────────────────────────────────


def merge_k_sorted(lists: List[List[int]]) -> List[int]:
    """Merge K sorted lists into one sorted list.

    Uses a min-heap to track the smallest unmerged element across all lists.

    Args:
        lists: List of sorted integer lists.

    Returns:
        A single merged sorted list.

    Time Complexity: O(N log K) where N = total elements, K = number of lists.
    Space Complexity: O(K) for the heap.

    Examples:
        >>> merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]])
        [1, 1, 2, 3, 4, 4, 5, 6]
        >>> merge_k_sorted([])
        []
        >>> merge_k_sorted([[], []])
        []
    """
    # Filter out empty lists
    lists = [lst for lst in lists if lst]
    if not lists:
        return []

    result: List[int] = []
    # Heap entries: (value, list_index, element_index)
    heap: List[tuple[int, int, int]] = []

    # Initialize heap with the first element of each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Push the next element from the same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result


# ─── 4. Find Median from Data Stream ────────────────────────────────────────


class MedianFinder:
    """Data structure that supports adding numbers and finding the median.

    Uses two heaps:
        - `low`: max-heap for the lower half of numbers.
        - `high`: min-heap for the upper half of numbers.

    Maintains invariant: len(low) == len(high) or len(low) == len(high) + 1.

    Time Complexities:
        - add_num: O(log n)
        - find_median: O(1)

    Space Complexity: O(n)

    Examples:
        >>> mf = MedianFinder()
        >>> mf.add_num(1)
        >>> mf.add_num(2)
        >>> mf.find_median()
        1.5
        >>> mf.add_num(3)
        >>> mf.find_median()
        2.0
    """

    def __init__(self) -> None:
        """Initialize the median finder."""
        # Max-heap (simulated with negatives) for lower half
        self._low: List[int] = []
        # Min-heap for upper half
        self._high: List[int] = []

    def add_num(self, num: int) -> None:
        """Add a number to the data stream.

        Args:
            num: Integer to add.

        Time Complexity: O(log n)
        """
        # Push to max-heap (low) first
        heapq.heappush(self._low, -num)

        # Move the largest of low to high
        if self._low:
            largest_low = -heapq.heappop(self._low)
            heapq.heappush(self._high, largest_low)

        # Balance: low should be same size or 1 larger than high
        if len(self._low) < len(self._high):
            smallest_high = heapq.heappop(self._high)
            heapq.heappush(self._low, -smallest_high)

    def find_median(self) -> float:
        """Return the median of current numbers.

        Returns:
            Median value.

        Raises:
            IndexError: If no numbers have been added.

        Time Complexity: O(1)

        Examples:
            >>> mf = MedianFinder()
            >>> mf.add_num(5)
            >>> mf.find_median()
            5.0
        """
        if not self._low:
            raise IndexError("No numbers added")

        if len(self._low) > len(self._high):
            return float(-self._low[0])
        return (-self._low[0] + self._high[0]) / 2.0


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

    # ── Top K Frequent ───────────────────────────────────────────────────────
    print("Top K Frequent:")
    result = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    check("k=2", sorted(result) == [1, 2])
    check("k=1", top_k_frequent([1], 1) == [1])

    # ── Kth Largest ──────────────────────────────────────────────────────────
    print("\nKth Largest:")
    check("k=2", kth_largest([3, 2, 1, 5, 6, 4], 2) == 5)
    check("k=4", kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4)
    check("k=1 (max)", kth_largest([10, 20, 30], 1) == 30)
    check("k=n (min)", kth_largest([10, 20, 30], 3) == 10)

    try:
        kth_largest([1, 2], 0)
        check("k=0 raises", False)
    except ValueError:
        check("k=0 raises", True)

    try:
        kth_largest([1, 2], 3)
        check("k>n raises", False)
    except ValueError:
        check("k>n raises", True)

    # Kth Smallest
    check("kth_smallest k=2", kth_smallest([3, 2, 1, 5, 6, 4], 2) == 2)
    check("kth_smallest k=1", kth_smallest([10, 20, 30], 1) == 10)

    # ── Merge K Sorted ───────────────────────────────────────────────────────
    print("\nMerge K Sorted Lists:")
    merged = merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]])
    check("basic merge", merged == [1, 1, 2, 3, 4, 4, 5, 6])
    check("empty lists", merge_k_sorted([]) == [])
    check("nested empty", merge_k_sorted([[], [], []]) == [])
    check("single list", merge_k_sorted([[1, 2, 3]]) == [1, 2, 3])

    # ── Median Finder ────────────────────────────────────────────────────────
    print("\nMedian Finder:")
    mf = MedianFinder()
    mf.add_num(1)
    check("single num median = 1.0", mf.find_median() == 1.0)
    mf.add_num(2)
    check("two nums median = 1.5", mf.find_median() == 1.5)
    mf.add_num(3)
    check("three nums median = 2.0", mf.find_median() == 2.0)

    mf2 = MedianFinder()
    mf2.add_num(-1)
    mf2.add_num(-2)
    mf2.add_num(-3)
    check("negative nums median = -2.0", mf2.find_median() == -2.0)

    mf3 = MedianFinder()
    mf3.add_num(5)
    mf3.add_num(15)
    mf3.add_num(1)
    mf3.add_num(3)
    check("four nums median", mf3.find_median() == 4.0)

    try:
        MedianFinder().find_median()
        check("empty find_median raises", False)
    except IndexError:
        check("empty find_median raises", True)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
