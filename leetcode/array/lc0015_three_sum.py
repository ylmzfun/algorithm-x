"""
LeetCode #15: 3Sum
https://leetcode.com/problems/3sum/

Given an integer array `nums`, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

The solution set must not contain duplicate triplets.

Constraints:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5

Approach 1: Brute Force
    Triple nested loop. O(n^3) time, O(1) space (ignoring output).

Approach 2: Sort + Two Pointers
    Sort the array, then for each element nums[i], use two pointers (left, right)
    to find pairs that sum to -nums[i]. Skip duplicates to avoid duplicate triplets.
    O(n^2) time, O(1) space (ignoring output / sort overhead).
"""

from typing import List


def three_sum_sort(nums: List[int]) -> List[List[int]]:
    """Sort + two-pointer: O(n^2) time, O(1) extra space."""
    nums.sort()
    n = len(nums)
    result: List[List[int]] = []

    for i in range(n - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Early termination: smallest possible sum > 0
        if nums[i] > 0:
            break

        target = -nums[i]
        left, right = i + 1, n - 1

        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicates for left and right
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1

    return result


# ── Default export ──
threeSum = three_sum_sort


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([-2, 0, 0, 2, 2], [[-2, 0, 2]]),
        ([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],
         [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2],
          [-2, -2, 4], [-2, 0, 2]]),
    ]

    all_pass = True
    for nums, expected in test_cases:
        result = three_sum_sort(nums)
        # Sort for comparison
        result_sorted = sorted([sorted(triplet) for triplet in result])
        expected_sorted = sorted([sorted(triplet) for triplet in expected])
        pass_flag = result_sorted == expected_sorted
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => {result}")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
