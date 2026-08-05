"""
LeetCode #560: Subarray Sum Equals K
https://leetcode.com/problems/subarray-sum-equals-k/

Given an array of integers `nums` and an integer `k`, return the total number of
subarrays whose sum equals to k.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

Approach 1: Prefix Sum + Hash Map
    Maintain a running prefix sum. For each position, check if
    (current_sum - k) has been seen before. The count of such occurrences gives
    the number of subarrays ending at the current position that sum to k.
    O(n) time, O(n) space.

Approach 2: Brute Force
    Check every subarray. O(n^2) time, O(1) space.
"""

from typing import List
from collections import defaultdict


def subarray_sum_prefix_hash(nums: List[int], k: int) -> int:
    """Prefix sum + hash map: O(n) time, O(n) space."""
    # Map prefix_sum → count of occurrences
    prefix_count = defaultdict(int)
    prefix_count[0] = 1  # Empty subarray has sum 0

    current_sum = 0
    count = 0

    for num in nums:
        current_sum += num
        # If current_sum - k exists, there are subarrays ending here that sum to k
        count += prefix_count.get(current_sum - k, 0)
        prefix_count[current_sum] += 1

    return count


def subarray_sum_brute(nums: List[int], k: int) -> int:
    """Brute force: O(n^2) time, O(1) space."""
    n = len(nums)
    count = 0

    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += nums[j]
            if current_sum == k:
                count += 1

    return count


# ── Default export ──
subarraySum = subarray_sum_prefix_hash


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1], 0, 0),
        ([-1, -1, 1], 0, 1),
        ([1, -1, 0], 0, 3),  # [], [1,-1], [0]
        ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
    ]

    all_pass = True
    for nums, k, expected in test_cases:
        r1 = subarray_sum_prefix_hash(nums, k)
        pass_flag = r1 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums}, k={k} => {r1} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
