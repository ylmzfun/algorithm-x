"""
State / Bitmask Dynamic Programming
======================================

DP where the state is represented compactly, often using bitmasks for
visited sets or grid coordinates.

Functions:
- tsp_bitmask        : Traveling Salesman Problem (DP with bitmask).
- min_path_sum       : Minimum path sum in a grid (top-left → bottom-right).
- unique_paths       : Number of unique paths in a grid.
- unique_paths_with_obstacles : Unique paths with obstacles.
- dungeon_game       : Minimum initial HP to rescue the princess.
"""

from typing import List


# ---------------------------------------------------------------------------
# Traveling Salesman Problem (DP + Bitmask)
# ---------------------------------------------------------------------------

def tsp_bitmask(dist: List[List[int]]) -> int:
    """
    Solve the Traveling Salesman Problem using DP with bitmask.

    Find the minimum cost to visit all cities exactly once and return to
    the starting city (city 0).

    dp[mask][i] = min cost to visit the set of cities represented by 'mask'
                  and end at city i, starting from city 0.

    Parameters
    ----------
    dist : List[List[int]]
        n×n distance matrix (symmetric, dist[i][i] = 0).

    Returns
    -------
    int
        Minimum tour cost.

    Time  : O(n²·2^n)
    Space : O(n·2^n)

    Example
    -------
    >>> tsp_bitmask([[0, 10, 15, 20],
    ...              [10, 0, 35, 25],
    ...              [15, 35, 0, 30],
    ...              [20, 25, 30, 0]])
    80   # 0→1→3→2→0: 10+25+30+15 = 80
    """
    n = len(dist)
    INF = 10**9
    # dp[mask][i]
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0

    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            if dp[mask][u] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v],
                                      dp[mask][u] + dist[u][v])

    # Return to start
    full_mask = (1 << n) - 1
    ans = INF
    for u in range(1, n):
        ans = min(ans, dp[full_mask][u] + dist[u][0])
    return ans


# ---------------------------------------------------------------------------
# Minimum Path Sum in Grid
# ---------------------------------------------------------------------------

def min_path_sum(grid: List[List[int]]) -> int:
    """
    Minimum path sum from top-left to bottom-right, moving only down or
    right.

    dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]).

    Parameters
    ----------
    grid : List[List[int]]
        2D grid of non-negative integers.

    Returns
    -------
    int
        Minimum path sum.

    Time  : O(rows × cols)
    Space : O(cols) with 1D optimisation.

    Example
    -------
    >>> min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    7   # 1→3→1→1→1 = 7
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    dp = [0] * cols

    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                dp[j] = grid[i][j]
            elif i == 0:
                dp[j] = dp[j - 1] + grid[i][j]
            elif j == 0:
                dp[j] = dp[j] + grid[i][j]
            else:
                dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]

    return dp[-1]


# ---------------------------------------------------------------------------
# Unique Paths
# ---------------------------------------------------------------------------

def unique_paths(m: int, n: int) -> int:
    """
    Number of unique paths from top-left to bottom-right of an m×n grid,
    moving only down or right.

    Combinatorially: C(m+n-2, m-1).

    Parameters
    ----------
    m : int
        Number of rows.
    n : int
        Number of columns.

    Returns
    -------
    int
        Number of unique paths.

    Time  : O(min(m, n))
    Space : O(1)

    Example
    -------
    >>> unique_paths(3, 7)
    28
    """
    import math
    return math.comb(m + n - 2, m - 1)


def unique_paths_with_obstacles(grid: List[List[int]]) -> int:
    """
    Number of unique paths from top-left to bottom-right with obstacles.

    grid[i][j] == 1 means obstacle; 0 means free.

    Parameters
    ----------
    grid : List[List[int]]
        2D grid with 0 (free) and 1 (obstacle).

    Returns
    -------
    int
        Number of unique paths.

    Time  : O(rows × cols)
    Space : O(cols)

    Example
    -------
    >>> unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    2
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    dp = [0] * cols
    dp[0] = 1 if grid[0][0] == 0 else 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    return dp[-1]


# ---------------------------------------------------------------------------
# Dungeon Game
# ---------------------------------------------------------------------------

def dungeon_game(dungeon: List[List[int]]) -> int:
    """
    Minimum initial health needed for the knight to rescue the princess.

    The knight starts at top-left (0, 0), the princess is at bottom-right.
    Each cell may increase or decrease HP.  At any point, HP must be >= 1.

    Work backwards (bottom-right → top-left):
        dp[i][j] = min HP needed at (i, j) before entering.

    Parameters
    ----------
    dungeon : List[List[int]]
        Grid of HP changes (negative = damage, positive = heal).

    Returns
    -------
    int
        Minimum initial HP.

    Time  : O(rows × cols)
    Space : O(cols)

    Example
    -------
    >>> dungeon_game([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]])
    7
    """
    if not dungeon or not dungeon[0]:
        return 1
    rows, cols = len(dungeon), len(dungeon[0])
    dp = [0] * cols

    for i in range(rows - 1, -1, -1):
        for j in range(cols - 1, -1, -1):
            if i == rows - 1 and j == cols - 1:
                dp[j] = max(1, 1 - dungeon[i][j])
            elif i == rows - 1:
                dp[j] = max(1, dp[j + 1] - dungeon[i][j])
            elif j == cols - 1:
                dp[j] = max(1, dp[j] - dungeon[i][j])
            else:
                dp[j] = max(1, min(dp[j], dp[j + 1]) - dungeon[i][j])
    return dp[0]


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== State / Bitmask DP Tests ===\n")

    # tsp_bitmask
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    assert tsp_bitmask(dist) == 80
    print("  PASS tsp_bitmask")

    # min_path_sum
    assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert min_path_sum([[1, 2], [1, 1]]) == 3
    print("  PASS min_path_sum")

    # unique_paths
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
    print("  PASS unique_paths")

    # unique_paths_with_obstacles
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert unique_paths_with_obstacles(grid) == 2
    grid2 = [[0, 1], [0, 0]]
    assert unique_paths_with_obstacles(grid2) == 1
    print("  PASS unique_paths_with_obstacles")

    # dungeon_game
    dg = [[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]
    assert dungeon_game(dg) == 7
    assert dungeon_game([[0]]) == 1
    assert dungeon_game([[-5]]) == 6
    print("  PASS dungeon_game")

    print("\nAll state DP tests completed!")
