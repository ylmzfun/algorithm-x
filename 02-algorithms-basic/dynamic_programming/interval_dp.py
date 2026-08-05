"""
Interval / Range Dynamic Programming
======================================

DP over intervals [i, j] where the optimal answer for a larger interval
depends on smaller sub-intervals.

Functions:
- matrix_chain_multiplication : Min scalar multiplications for matrix product.
- optimal_bst                 : Min search cost for an Optimal BST.
- burst_balloons              : Max coins from bursting balloons.
- stone_game                  : Predict winner of the stone pile game.
"""

from typing import List


# ---------------------------------------------------------------------------
# Matrix Chain Multiplication
# ---------------------------------------------------------------------------

def matrix_chain_multiplication(dims: List[int]) -> int:
    """
    Minimum number of scalar multiplications needed to multiply a chain of
    matrices A₁ × A₂ × … × Aₙ, where the dimensions of A_i are
    dims[i-1] × dims[i].

    Parameters
    ----------
    dims : List[int]
        Array of dimensions: [p₀, p₁, …, pₙ] where A_i is p_{i-1} × p_i.

    Returns
    -------
    int
        Minimum scalar multiplications.

    Time  : O(n³)
    Space : O(n²)

    Example
    -------
    >>> matrix_chain_multiplication([10, 30, 5, 60])
    4500   # (A₁(A₂A₃)) = 30×5×60 + 10×30×60 = 9000 + 18000 = 27000
           # ((A₁A₂)A₃) = 10×30×5 + 10×5×60 = 1500 + 3000 = 4500 ✓
    """
    n = len(dims) - 1
    if n <= 1:
        return 0

    # dp[i][j] = min cost to multiply matrices i..j (1-indexed)
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                dp[i][j] = min(dp[i][j], cost)

    return dp[1][n]


# ---------------------------------------------------------------------------
# Optimal Binary Search Tree
# ---------------------------------------------------------------------------

def optimal_bst(keys: List[int], freq: List[int]) -> int:
    """
    Minimum search cost for an Optimal Binary Search Tree given keys and
    their access frequencies.

    Uses Knuth's optimisation to reduce O(n³) to O(n²).

    Parameters
    ----------
    keys : List[int]
        Sorted keys (used only for size; values not directly needed by DP).
    freq : List[int]
        Access frequency for each key.

    Returns
    -------
    int
        Minimum total search cost.

    Time  : O(n²) with Knuth optimisation.
    Space : O(n²)

    Example
    -------
    >>> optimal_bst([10, 20, 30, 40], [4, 2, 6, 3])
    26
    """
    n = len(keys)
    # Prefix sum of frequencies
    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + freq[i - 1]

    # dp[i][j] = min cost for keys i..j (0-indexed)
    dp = [[0] * n for _ in range(n)]
    # root[i][j] = optimal root for keys i..j (Knuth)
    root = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = freq[i]
        root[i][i] = i

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            freq_sum = pref[j + 1] - pref[i]
            # Knuth's optimisation limits k range
            for k in range(root[i][j - 1] if j > i else i,
                           min(root[i + 1][j] if i < j else j, j) + 1):
                left = dp[i][k - 1] if k > i else 0
                right = dp[k + 1][j] if k < j else 0
                cost = left + right + freq_sum
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    root[i][j] = k

    return dp[0][n - 1]


# ---------------------------------------------------------------------------
# Burst Balloons
# ---------------------------------------------------------------------------

def burst_balloons(nums: List[int]) -> int:
    """
    Maximum coins obtainable by bursting balloons.  When balloon i is
    burst, coins = nums[left] * nums[i] * nums[right] (with implicit 1s
    at boundaries).

    dp[i][j] = max coins from bursting all balloons in (i, j) (exclusive).

    Parameters
    ----------
    nums : List[int]
        Balloon values.

    Returns
    -------
    int
        Maximum coins.

    Time  : O(n³)
    Space : O(n²)

    Example
    -------
    >>> burst_balloons([3, 1, 5, 8])
    167   # nums = [1,3,1,5,8,1]; burst 1→1*1*3=3, burst 5→3*5*8=120,
          # burst 3→1*3*8=24, burst 8→1*8*1=8, burst 1→1*1*1=1? No...
          # Better: burst 1→3*1*5=15, burst 5→3*5*8=120, burst 3→1*3*8=24,
          # burst 8→1*8*1=8. Total=167.
    """
    n = len(nums)
    # Pad with 1 on both ends
    padded = [1] + nums + [1]
    dp = [[0] * (n + 2) for _ in range(n + 2)]

    for length in range(1, n + 1):
        for left in range(1, n - length + 2):
            right = left + length - 1
            for k in range(left, right + 1):
                coins = (dp[left][k - 1] + dp[k + 1][right] +
                         padded[left - 1] * padded[k] * padded[right + 1])
                dp[left][right] = max(dp[left][right], coins)

    return dp[1][n]


# ---------------------------------------------------------------------------
# Stone Game
# ---------------------------------------------------------------------------

def stone_game(piles: List[int]) -> bool:
    """
    Determine if the first player can win the stone game.

    Players take turns taking a pile from either end.  Both play optimally.
    The total number of stones is odd, so there are no ties.

    dp[i][j] = max net advantage (first - second) for sub-array piles[i:j+1].

    Parameters
    ----------
    piles : List[int]
        Number of stones in each pile.

    Returns
    -------
    bool
        True if first player wins.

    Time  : O(n²)
    Space : O(n²)

    Example
    -------
    >>> stone_game([5, 3, 4, 5])
    True
    """
    n = len(piles)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = piles[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(piles[i] - dp[i + 1][j],
                           piles[j] - dp[i][j - 1])

    return dp[0][n - 1] > 0


# ---------------------------------------------------------------------------
# Remove Boxes (simplified — returns max score)
# ---------------------------------------------------------------------------

def remove_boxes(boxes: List[int]) -> int:
    """
    Maximum points obtainable by removing boxes.  Each turn, you may remove
    k contiguous boxes of the same colour and earn k² points.

    dp[l][r][k] = max points from boxes[l:r+1] with k boxes of the same
    colour as boxes[l] appended to the left.

    Parameters
    ----------
    boxes : List[int]
        Box colours (integers).

    Returns
    -------
    int
        Maximum points.

    Time  : O(n⁴) / O(n³) with optimisation.
    Space : O(n³)

    Example
    -------
    >>> remove_boxes([1, 3, 2, 2, 2, 3, 4, 3, 1])
    23
    """
    n = len(boxes)
    # dp[l][r][k] — note: using memoisation instead of full 3D array
    from functools import lru_cache

    @lru_cache(None)
    def dfs(l: int, r: int, k: int) -> int:
        if l > r:
            return 0
        # Merge consecutive same-colour boxes
        while l < r and boxes[l + 1] == boxes[l]:
            l += 1
            k += 1

        # Option 1: remove the k+1 boxes now
        ans = (k + 1) * (k + 1) + dfs(l + 1, r, 0)

        # Option 2: merge with later boxes of the same colour
        for m in range(l + 1, r + 1):
            if boxes[m] == boxes[l]:
                ans = max(ans, dfs(l + 1, m - 1, 0) + dfs(m, r, k + 1))
        return ans

    return dfs(0, n - 1, 0)


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Interval DP Tests ===\n")

    # matrix_chain_multiplication
    assert matrix_chain_multiplication([10, 30, 5, 60]) == 4500
    assert matrix_chain_multiplication([40, 20, 30, 10, 30]) == 26000
    assert matrix_chain_multiplication([10, 20]) == 0
    print("  PASS matrix_chain_multiplication")

    # optimal_bst
    assert optimal_bst([10, 20, 30, 40], [4, 2, 6, 3]) == 26
    assert optimal_bst([10, 20], [34, 50]) == 118  # freq[0]=34, freq[1]=50
    print("  PASS optimal_bst")

    # burst_balloons
    assert burst_balloons([3, 1, 5, 8]) == 167
    assert burst_balloons([1, 5]) == 10
    print("  PASS burst_balloons")

    # stone_game
    assert stone_game([5, 3, 4, 5]) == True
    assert stone_game([3, 7, 2, 3]) == True
    print("  PASS stone_game")

    # remove_boxes
    assert remove_boxes([1, 3, 2, 2, 2, 3, 4, 3, 1]) == 23
    assert remove_boxes([1, 1, 1]) == 9
    assert remove_boxes([1]) == 1
    print("  PASS remove_boxes")

    print("\nAll interval DP tests completed!")
