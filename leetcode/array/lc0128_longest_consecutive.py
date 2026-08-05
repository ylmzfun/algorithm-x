"""
LeetCode #128: Longest Consecutive Sequence
https://leetcode.com/problems/longest-consecutive-sequence/

Given an unsorted array of integers `nums`, return the length of the longest
consecutive elements sequence. You must write an algorithm that runs in O(n) time.

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

Approach: Hash Set
    Insert all numbers into a hash set. For each number, if it's the start of a
    sequence (nums[i] - 1 not in set), count consecutive numbers upward.
    Each element is visited at most twice. O(n) time, O(n) space.
"""

from typing import List


def longest_consecutive(nums: List[int]) -> int:
    """Hash set approach: O(n) time, O(n) space."""
    if not nums:
        return 0

    num_set = set(nums)
    max_len = 0

    for num in num_set:
        # Only start counting from sequence beginnings
        if num - 1 not in num_set:
            current_num = num
            current_len = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_len += 1

            max_len = max(max_len, current_len)

    return max_len


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),
        ([1, 2, 0, 1], 3),
        ([9, 1, -3, 2, 4, 8, 3, -1, 6, -2, -4, 7, 5, -8, 0, -6],
         14),  # -4 through 9 = 14 consecutive elements
        ([0, 0], 1),
    ]

    all_pass = True
    for nums, expected in test_cases:
        result = longest_consecutive(nums)
        pass_flag = result == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
