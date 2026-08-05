"""
LeetCode #347: Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array `nums` and an integer `k`, return the k most frequent elements.
You may return the answer in any order.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in the range [1, the number of unique elements in the array].
- It is guaranteed that the answer is unique.

Approach 1: Bucket Sort
    Count frequencies. Use an array of buckets where bucket[i] contains elements
    with frequency i. Collect from the highest frequency bucket downward until
    we have k elements. O(n) time, O(n) space.

Approach 2: Heap (Min-Heap of size k)
    Count frequencies, then maintain a min-heap of size k sorted by frequency.
    O(n log k) time, O(n + k) space.
"""

from typing import List
from collections import Counter
import heapq


def top_k_frequent_bucket(nums: List[int], k: int) -> List[int]:
    """Bucket sort: O(n) time, O(n) space."""
    freq = Counter(nums)
    n = len(nums)

    # Bucket where index = frequency, value = list of elements with that frequency
    buckets: List[List[int]] = [[] for _ in range(n + 1)]
    for num, cnt in freq.items():
        buckets[cnt].append(num)

    result: List[int] = []
    # Collect from highest frequency down
    for cnt in range(n, 0, -1):
        for num in buckets[cnt]:
            result.append(num)
            if len(result) == k:
                return result

    return result


def top_k_frequent_heap(nums: List[int], k: int) -> List[int]:
    """Min-heap of size k: O(n log k) time, O(n + k) space."""
    freq = Counter(nums)

    # Min-heap based on frequency; store (freq, num)
    heap: List[tuple[int, int]] = []
    for num, cnt in freq.items():
        heapq.heappush(heap, (cnt, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for _, num in heap]


# ── Default export ──
topKFrequent = top_k_frequent_bucket


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 1, 1, 2, 2, 3], 2, [1, 2]),
        ([1], 1, [1]),
        ([4, 1, -1, 2, -1, 2, 3], 2, [-1, 2]),
        ([1, 2, 2, 3, 3, 3], 1, [3]),
        ([5, 5, 5, 6, 6, 7], 2, [5, 6]),
    ]

    all_pass = True
    for nums, k, expected in test_cases:
        r1 = top_k_frequent_bucket(nums, k)
        r2 = top_k_frequent_heap(nums, k)
        pass_flag = sorted(r1) == sorted(expected) and sorted(r2) == sorted(expected)
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums}, k={k} => bucket={r1}, heap={r2} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
