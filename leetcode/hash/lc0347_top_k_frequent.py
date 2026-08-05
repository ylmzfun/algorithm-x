"""
347. Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array nums and an integer k, return the k most frequent
elements. You may return the answer in any order.
"""

from __future__ import annotations
from collections import Counter
import heapq


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Min-Heap of size k
# Count frequencies, then keep a min-heap of the k largest.
# Time: O(N log K)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def top_k_frequent_heap(nums: list[int], k: int) -> list[int]:
    """Min-heap of size k: O(N log K)."""
    freq = Counter(nums)
    heap: list[tuple[int, int]] = []
    for num, cnt in freq.items():
        heapq.heappush(heap, (cnt, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for _, num in heap]


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: Bucket Sort
# Time: O(N)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def top_k_frequent_bucket(nums: list[int], k: int) -> list[int]:
    """Bucket sort by frequency: O(N)."""
    freq = Counter(nums)
    n = len(nums)

    # bucket[i] = numbers appearing i times (max frequency ≤ n)
    buckets: list[list[int]] = [[] for _ in range(n + 1)]
    for num, cnt in freq.items():
        buckets[cnt].append(num)

    result: list[int] = []
    for cnt in range(n, 0, -1):
        for num in buckets[cnt]:
            result.append(num)
            if len(result) == k:
                return result
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, nums: list[int], k: int, expected: set[int]):
        methods = [
            ("Heap", top_k_frequent_heap),
            ("Bucket", top_k_frequent_bucket),
        ]
        for name, fn in methods:
            result = fn(nums, k)
            ok = set(result) == expected
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [1, 1, 1, 2, 2, 3], 2, {1, 2})
    test("Example 2", [1], 1, {1})
    test("Example 3", [4, 1, -1, 2, -1, 2, 3], 2, {-1, 2})
    print("\nAll top k frequent tests completed.")
