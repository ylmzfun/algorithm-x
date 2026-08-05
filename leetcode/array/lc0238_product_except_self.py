"""
LeetCode #238: Product of Array Except Self
https://leetcode.com/problems/product-of-array-except-self/

Given an integer array `nums`, return an array `answer` such that answer[i] is equal
to the product of all the elements of nums except nums[i]. The product of any prefix
or suffix of nums fits in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division
operation.

Constraints:
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30

Approach 1: Two-pass with Prefix and Suffix Products
    First pass: compute prefix products left to right (answer[i] = product of all
               elements to the left of i).
    Second pass: multiply by suffix products right to left.
    O(n) time, O(1) space (output array not counted as extra).

Approach 2: Separate Left/Right Arrays
    Precompute left_products and right_products arrays, then multiply.
    O(n) time, O(n) space.
"""

from typing import List


def product_except_self_two_pass(nums: List[int]) -> List[int]:
    """Two-pass prefix/suffix: O(n) time, O(1) extra space."""
    n = len(nums)
    answer = [1] * n

    # First pass: prefix products (left of i)
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    # Second pass: multiply by suffix products (right of i)
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer


def product_except_self_arrays(nums: List[int]) -> List[int]:
    """Left and right arrays: O(n) time, O(n) space."""
    n = len(nums)
    left = [1] * n
    right = [1] * n

    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]

    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] * nums[i + 1]

    return [left[i] * right[i] for i in range(n)]


# ── Default export ──
productExceptSelf = product_except_self_two_pass


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([2, 3], [3, 2]),
        ([0, 0], [0, 0]),
        ([1, 1, 1, 1], [1, 1, 1, 1]),
    ]

    all_pass = True
    for nums, expected in test_cases:
        r1 = product_except_self_two_pass(nums)
        r2 = product_except_self_arrays(nums)
        pass_flag = r1 == expected and r2 == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | nums={nums} => 2pass={r1}, arrays={r2} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
