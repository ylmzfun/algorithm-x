"""
Knapsack and Subset-Sum Problems
=================================

Fundamental DP problems involving selecting items with constraints.

Functions:
- knapsack_01_2d            : 0/1 knapsack with 2D DP.
- knapsack_01_1d            : 0/1 knapsack with 1D space optimisation.
- knapsack_01_with_items    : Returns max value AND selected items.
- unbounded_knapsack        : Unlimited copies of each item.
- partition_equal_subset_sum: Can array be partitioned into equal-sum halves?
- target_sum                : Number of ways to assign +/- to reach target.
- coin_change_min           : Minimum coins for amount (unbounded).
- coin_change_ways          : Number of combinations to make amount.
"""

from typing import List, Tuple


# ---------------------------------------------------------------------------
# 0/1 Knapsack — 2D DP
# ---------------------------------------------------------------------------

def knapsack_01_2d(weights: List[int], values: List[int],
                   capacity: int) -> int:
    """
    Solve the 0/1 knapsack problem using 2D DP.

    Parameters
    ----------
    weights : List[int]
        Weight of each item.
    values : List[int]
        Value of each item.
    capacity : int
        Maximum weight the knapsack can hold.

    Returns
    -------
    int
        Maximum total value achievable.

    Time  : O(n × capacity)
    Space : O(n × capacity)
    """
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(capacity + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


# ---------------------------------------------------------------------------
# 0/1 Knapsack — 1D space-optimised
# ---------------------------------------------------------------------------

def knapsack_01_1d(weights: List[int], values: List[int],
                   capacity: int) -> int:
    """
    Solve the 0/1 knapsack problem using a 1D DP array (space-optimised).

    Parameters
    ----------
    weights : List[int]
        Weight of each item.
    values : List[int]
        Value of each item.
    capacity : int
        Maximum weight.

    Returns
    -------
    int
        Maximum total value.

    Time  : O(n × capacity)
    Space : O(capacity)
    """
    dp = [0] * (capacity + 1)
    for w_i, v_i in zip(weights, values):
        # Iterate backwards so each item is used at most once
        for w in range(capacity, w_i - 1, -1):
            dp[w] = max(dp[w], dp[w - w_i] + v_i)
    return dp[capacity]


# ---------------------------------------------------------------------------
# 0/1 Knapsack with Item Reconstruction
# ---------------------------------------------------------------------------

def knapsack_01_with_items(
    weights: List[int], values: List[int], capacity: int
) -> Tuple[int, List[int]]:
    """
    Solve 0/1 knapsack and return both the max value and the indices of
    selected items (0-based).

    Parameters
    ----------
    weights : List[int]
    values : List[int]
    capacity : int

    Returns
    -------
    Tuple[int, List[int]]
        (max_value, [indices of selected items]).

    Time  : O(n × capacity)
    Space : O(n × capacity)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(capacity + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruct selected items
    selected: List[int] = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    selected.reverse()

    return dp[n][capacity], selected


# ---------------------------------------------------------------------------
# Unbounded Knapsack
# ---------------------------------------------------------------------------

def unbounded_knapsack(weights: List[int], values: List[int],
                       capacity: int) -> int:
    """
    Solve the unbounded knapsack problem (unlimited copies of each item).

    Parameters
    ----------
    weights : List[int]
    values : List[int]
    capacity : int

    Returns
    -------
    int
        Maximum value.

    Time  : O(n × capacity)
    Space : O(capacity)

    Example
    -------
    >>> unbounded_knapsack([2, 3, 4], [4, 5, 6], 7)
    14   # three of item 0 (weight 2, value 4) + one of item 0...
          # Actually: items 2+2+3 = weight 7, value 4+4+5 = 13
          # Let's recalculate: 7 capacity -> best is weight 2+2+3=7, value 4+4+5=13
          # Wait: weight 2*3=6, value 4*3=12, weight 4+3=7, value 6+5=11...
          # Best: weight 2+2+3=7, value 4+4+5=13 ✓
    """
    dp = [0] * (capacity + 1)
    for w in range(1, capacity + 1):
        for w_i, v_i in zip(weights, values):
            if w_i <= w:
                dp[w] = max(dp[w], dp[w - w_i] + v_i)
    return dp[capacity]


# ---------------------------------------------------------------------------
# Partition Equal Subset Sum
# ---------------------------------------------------------------------------

def partition_equal_subset_sum(nums: List[int]) -> bool:
    """
    Determine if the array can be partitioned into two subsets with equal sum.

    Reduces to: can we find a subset whose sum = total_sum / 2?

    Parameters
    ----------
    nums : List[int]
        Positive integers.

    Returns
    -------
    bool
        True if an equal-sum partition exists.

    Time  : O(n × sum/2)
    Space : O(sum/2)

    Example
    -------
    >>> partition_equal_subset_sum([1, 5, 11, 5])
    True   # {1, 5, 5} and {11} both sum to 11
    """
    total = sum(nums)
    if total % 2 != 0:
        return False

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]

    return dp[target]


# ---------------------------------------------------------------------------
# Target Sum (+/- assignments)
# ---------------------------------------------------------------------------

def target_sum(nums: List[int], target: int) -> int:
    """
    Count the number of ways to assign '+' and '-' to elements of ``nums``
    such that the total equals ``target``.

    Equivalent to subset sum: find subset P such that
        sum(P) - sum(N) = target
    =>  sum(P) = (target + sum(nums)) // 2

    Parameters
    ----------
    nums : List[int]
        Array of non-negative integers.
    target : int
        Desired total.

    Returns
    -------
    int
        Number of expression combinations.

    Time  : O(n × s) where s = (target + sum) // 2.
    Space : O(s)

    Example
    -------
    >>> target_sum([1, 1, 1, 1, 1], 3)
    5
    """
    total = sum(nums)
    if target > total or (target + total) % 2 != 0:
        return 0

    s = (target + total) // 2
    dp = [0] * (s + 1)
    dp[0] = 1

    for num in nums:
        for w in range(s, num - 1, -1):
            dp[w] += dp[w - num]

    return dp[s]


# ---------------------------------------------------------------------------
# Coin Change — Minimum Coins
# ---------------------------------------------------------------------------

def coin_change_min(coins: List[int], amount: int) -> int:
    """
    Minimum number of coins needed to make ``amount`` (unbounded knapsack).

    Parameters
    ----------
    coins : List[int]
        Coin denominations.
    amount : int
        Target amount.

    Returns
    -------
    int
        Minimum coins, or -1 if impossible.

    Time  : O(n × amount)
    Space : O(amount)

    Example
    -------
    >>> coin_change_min([1, 2, 5], 11)
    3   # 5 + 5 + 1
    """
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != INF else -1


# ---------------------------------------------------------------------------
# Coin Change — Number of Ways
# ---------------------------------------------------------------------------

def coin_change_ways(coins: List[int], amount: int) -> int:
    """
    Number of combinations that make up ``amount`` (unbounded knapsack,
    order-independent).

    Parameters
    ----------
    coins : List[int]
        Coin denominations.
    amount : int
        Target amount.

    Returns
    -------
    int
        Number of ways.

    Time  : O(n × amount)
    Space : O(amount)

    Example
    -------
    >>> coin_change_ways([1, 2, 5], 5)
    4   # {5}, {2+2+1}, {2+1+1+1}, {1+1+1+1+1}
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]

    return dp[amount]


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Knapsack & Subset-Sum Tests ===\n")

    # 0/1 knapsack
    w = [2, 3, 4, 5]
    v = [3, 4, 5, 6]
    assert knapsack_01_2d(w, v, 5) == 7  # item 0+1
    assert knapsack_01_1d(w, v, 5) == 7
    val, items = knapsack_01_with_items(w, v, 5)
    assert val == 7 and sorted(items) == [0, 1]
    print("  PASS knapsack_01 (2D, 1D, with items)")

    # Unbounded knapsack
    assert unbounded_knapsack([2, 3, 4], [4, 5, 6], 7) == 13  # 2+2+3: 4+4+5=13
    print("  PASS unbounded_knapsack")

    # Partition equal subset sum
    assert partition_equal_subset_sum([1, 5, 11, 5]) == True
    assert partition_equal_subset_sum([1, 2, 3, 5]) == False
    print("  PASS partition_equal_subset_sum")

    # Target sum
    assert target_sum([1, 1, 1, 1, 1], 3) == 5
    assert target_sum([1], 1) == 1
    print("  PASS target_sum")

    # Coin change min
    assert coin_change_min([1, 2, 5], 11) == 3
    assert coin_change_min([2], 3) == -1
    print("  PASS coin_change_min")

    # Coin change ways
    assert coin_change_ways([1, 2, 5], 5) == 4
    assert coin_change_ways([2], 3) == 0
    print("  PASS coin_change_ways")

    print("\nAll knapsack tests completed!")
