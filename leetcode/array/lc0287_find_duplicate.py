"""
LeetCode #287: Find the Duplicate Number
https://leetcode.com/problems/find-the-duplicate-number/

Given an array of integers `nums` containing n + 1 integers where each integer is in
the range [1, n] inclusive. There is only one repeated number in nums, return this
repeated number.

You must solve the problem without modifying the array nums and using only constant
extra space.

Constraints:
- 1 <= n <= 10^5
- nums.length == n + 1
- 1 <= nums[i] <= n
- All the integers in nums appear only once except for precisely one integer which
  appears two or more times.

Approach 1: Floyd's Cycle Detection (Tortoise and Hare)
    Treat the array as a linked list where nums[i] points to the node at index
    nums[i]. Since there's a duplicate, there's a cycle. Find the cycle entrance
    which is the duplicate number.
    O(n) time, O(1) space.

Approach 2: Binary Search on Value Range
    Count numbers <= mid; if count > mid, the duplicate is in [1, mid].
    O(n log n) time, O(1) space.
"""

from typing import List


def find_duplicate_floyd(nums: List[int]) -> int:
    """Floyd's cycle detection: O(n) time, O(1) space."""
    # Phase 1: Find intersection point inside the cycle
    slow = nums[0]
    fast = nums[0]

    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find the entrance of the cycle (the duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow


def find_duplicate_binary_search(nums: List[int]) -> int:
    """Binary search on value range: O(n log n) time, O(1) space."""
    left, right = 1, len(nums) - 1

    while left < right:
        mid = (left + right) // 2
        # Count numbers <= mid
        count = sum(1 for x in nums if x <= mid)

        if count > mid:
            right = mid  # Duplicate is in [left, mid]
        else:
            left = mid + 1  # Duplicate is in [mid+1, right]

    return left


# ── Default export ──
findDuplicate = find_duplicate_floyd


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 3, 4, 2, 2], 2),
        ([3, 1, 3, 4, 2], 3),
        ([3, 3, 3, 3, 3], 3),
        ([1, 1], 1),
        ([2, 2, 2, 2, 2], 2),
    ]

    all_pass = True
    for nums, expected in test_cases:
        r1 = find_duplicate_floyd(nums)
        r2 = find_duplicate_binary_search(nums)
        pass_flag = r1 == expected and r2 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => floyd={r1}, bs={r2} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
