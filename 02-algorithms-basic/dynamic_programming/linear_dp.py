"""
Linear / 1D Dynamic Programming
=================================

Classic DP problems that can be solved with a 1D state array (or constant
space for some).

Functions:
- climb_stairs           : Number of ways to climb n stairs (1 or 2 steps).
- house_robber           : Max loot from non-adjacent houses.
- house_robber_ii        : Circular street version.
- max_subarray           : Kadane's algorithm — maximum sub-array sum.
- longest_increasing_subsequence : LIS O(n²) and O(n log n).
- russian_doll_envelopes : Maximum number of envelopes that can be nested.
"""

import bisect
from typing import List


# ---------------------------------------------------------------------------
# Climbing Stairs
# ---------------------------------------------------------------------------

def climb_stairs(n: int) -> int:
    """
    Number of distinct ways to climb to the top of a staircase with n steps,
    taking 1 or 2 steps at a time.

    This is the Fibonacci sequence: dp[i] = dp[i-1] + dp[i-2].

    Parameters
    ----------
    n : int
        Number of stairs.

    Returns
    -------
    int
        Number of ways.

    Time  : O(n)
    Space : O(1)

    Example
    -------
    >>> climb_stairs(3)
    3   # (1,1,1), (1,2), (2,1)
    """
    if n <= 2:
        return max(1, n)
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# ---------------------------------------------------------------------------
# House Robber
# ---------------------------------------------------------------------------

def house_robber(nums: List[int]) -> int:
    """
    Maximum amount of money you can rob from a row of houses without
    robbing two adjacent houses.

    dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    Parameters
    ----------
    nums : List[int]
        Amount of money in each house.

    Returns
    -------
    int
        Maximum loot.

    Time  : O(n)
    Space : O(1)

    Example
    -------
    >>> house_robber([2, 7, 9, 3, 1])
    12   # Rob house 1 (7) + house 3 (3) + house 5? No: rob 2(7)+4(3)+5(1)=11...
          # Actually rob 1(2)+3(9)+5(1)=12, or 2(7)+4(3)=10
          # best: rob 1(2), 3(9), 5(1) = 12 ✓
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
    return prev1


# ---------------------------------------------------------------------------
# House Robber II (circular)
# ---------------------------------------------------------------------------

def _rob_linear(nums: List[int]) -> int:
    """Helper: rob a linear street."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
    return prev1


def house_robber_ii(nums: List[int]) -> int:
    """
    House Robber on a **circular** street: first and last houses are
    adjacent.

    Solution: max of robbing houses [0, n-2] or [1, n-1].

    Parameters
    ----------
    nums : List[int]

    Returns
    -------
    int
        Maximum loot.

    Time  : O(n)
    Space : O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    return max(_rob_linear(nums[:-1]), _rob_linear(nums[1:]))


# ---------------------------------------------------------------------------
# Maximum Sub-array (Kadane's Algorithm)
# ---------------------------------------------------------------------------

def max_subarray(nums: List[int]) -> int:
    """
    Find the contiguous sub-array with the largest sum (Kadane's algorithm).

    Parameters
    ----------
    nums : List[int]
        Array of integers.

    Returns
    -------
    int
        Maximum sub-array sum.

    Time  : O(n)
    Space : O(1)

    Example
    -------
    >>> max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6   # sub-array [4, -1, 2, 1]
    """
    cur_max = global_max = nums[0]
    for x in nums[1:]:
        cur_max = max(x, cur_max + x)
        global_max = max(global_max, cur_max)
    return global_max


# ---------------------------------------------------------------------------
# Longest Increasing Subsequence (LIS)
# ---------------------------------------------------------------------------

def longest_increasing_subsequence(nums: List[int]) -> int:
    """
    Length of the longest strictly increasing subsequence — O(n²) DP.

    Parameters
    ----------
    nums : List[int]

    Returns
    -------
    int
        Length of LIS.

    Time  : O(n²)
    Space : O(n)

    Example
    -------
    >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
    4   # [2, 3, 7, 101]
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def longest_increasing_subsequence_nlogn(nums: List[int]) -> int:
    """
    Length of the longest strictly increasing subsequence — O(n log n)
    using patience sorting.

    Maintains a list ``tails`` where tails[i] = smallest tail of all
    increasing subsequences of length i+1.

    Parameters
    ----------
    nums : List[int]

    Returns
    -------
    int
        Length of LIS.

    Time  : O(n log n)
    Space : O(n)
    """
    tails: List[int] = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)


# ---------------------------------------------------------------------------
# Russian Doll Envelopes
# ---------------------------------------------------------------------------

def russian_doll_envelopes(envelopes: List[List[int]]) -> int:
    """
    Maximum number of envelopes that can be nested (Russian doll).

    An envelope (w1, h1) fits inside (w2, h2) iff w1 < w2 and h1 < h2.

    Reduces to LIS after sorting by width ascending and height descending
    (the descending height ensures envelopes of equal width cannot nest).

    Parameters
    ----------
    envelopes : List[List[int]]
        List of [width, height].

    Returns
    -------
    int
        Maximum nesting depth.

    Time  : O(n log n)
    Space : O(n)

    Example
    -------
    >>> russian_doll_envelopes([[5, 4], [6, 4], [6, 7], [2, 3]])
    3   # [2,3] -> [5,4] -> [6,7]
    """
    if not envelopes:
        return 0
    # Sort: width asc, height desc (so same-width cannot nest)
    envelopes.sort(key=lambda x: (x[0], -x[1]))
    heights = [h for _, h in envelopes]
    return longest_increasing_subsequence_nlogn(heights)


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Linear DP Tests ===\n")

    # climb_stairs
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
    print("  PASS climb_stairs")

    # house_robber
    assert house_robber([1, 2, 3, 1]) == 4  # rob 1 and 3
    assert house_robber([2, 7, 9, 3, 1]) == 12
    assert house_robber([]) == 0
    print("  PASS house_robber")

    # house_robber_ii
    assert house_robber_ii([2, 3, 2]) == 3
    assert house_robber_ii([1, 2, 3, 1]) == 4
    print("  PASS house_robber_ii")

    # max_subarray
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray([1]) == 1
    assert max_subarray([5, 4, -1, 7, 8]) == 23
    print("  PASS max_subarray")

    # LIS
    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert longest_increasing_subsequence_nlogn([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert longest_increasing_subsequence_nlogn([0, 1, 0, 3, 2, 3]) == 4
    print("  PASS longest_increasing_subsequence (both)")

    # russian_doll_envelopes
    assert russian_doll_envelopes([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3
    assert russian_doll_envelopes([[1, 1], [1, 1], [1, 1]]) == 1
    print("  PASS russian_doll_envelopes")

    print("\nAll linear DP tests completed!")
