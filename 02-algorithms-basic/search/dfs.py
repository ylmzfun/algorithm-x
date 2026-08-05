"""
Depth-First Search (DFS) Algorithms
====================================

DFS explores as far as possible along each branch before backtracking.
It can be implemented recursively (implicit call stack) or iteratively
(explicit stack).

Functions:
- dfs_recursive     : Generic DFS on adjacency-list graph.
- dfs_iterative     : Generic DFS with explicit stack.
- flood_fill        : Fill a connected region in a 2D grid (DFS/recursive).
- num_islands       : Count connected components of '1's in a grid.
- surrounded_regions: Capture regions surrounded by 'X's (connected to border
                       are not captured).
- word_search       : Search for a word in a 2D character board.
"""

from typing import List, Set, Dict, Optional


# ---------------------------------------------------------------------------
# Generic DFS (recursive)
# ---------------------------------------------------------------------------

def dfs_recursive(graph: Dict[int, List[int]], start: int,
                  visited: Optional[Set[int]] = None) -> Set[int]:
    """
    Perform recursive DFS on a graph and return reachable nodes.

    Parameters
    ----------
    graph : Dict[int, List[int]]
        Adjacency list.
    start : int
        Starting node.
    visited : Optional[Set[int]]
        Already-visited set (used for multiple components).

    Returns
    -------
    Set[int]
        Set of all nodes reachable from `start`.

    Time  : O(V + E)
    Space : O(V)
    """
    if visited is None:
        visited = set()

    def _dfs(u: int) -> None:
        visited.add(u)  # type: ignore[union-attr]
        for v in graph.get(u, []):
            if v not in visited:
                _dfs(v)

    _dfs(start)
    return visited  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Generic DFS (iterative)
# ---------------------------------------------------------------------------

def dfs_iterative(graph: Dict[int, List[int]], start: int) -> Set[int]:
    """
    Perform iterative DFS on a graph using an explicit stack.

    Parameters
    ----------
    graph : Dict[int, List[int]]
        Adjacency list.
    start : int
        Starting node.

    Returns
    -------
    Set[int]
        Nodes reachable from `start`.

    Time  : O(V + E)
    Space : O(V)
    """
    visited: Set[int] = set()
    stack: List[int] = [start]
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            # Push neighbours in reverse order for natural DFS order
            for v in reversed(graph.get(u, [])):
                if v not in visited:
                    stack.append(v)
    return visited


# ---------------------------------------------------------------------------
# Flood Fill
# ---------------------------------------------------------------------------

def flood_fill(image: List[List[int]], sr: int, sc: int,
               new_color: int) -> List[List[int]]:
    """
    Perform flood fill on a 2D grid starting at (sr, sc).  Changes the
    colour of the starting pixel and all 4-directionally connected pixels
    of the same original colour to `new_color`.

    Parameters
    ----------
    image : List[List[int]]
        2D grid of integer colours.
    sr, sc : int
        Starting row and column.
    new_color : int
        Colour to fill with.

    Returns
    -------
    List[List[int]]
        The modified image (same list, modified in place for efficiency,
        but returned for chaining).

    Time  : O(rows × cols)
    Space : O(rows × cols) worst-case recursion stack.
    """
    if not image or not image[0]:
        return image
    rows, cols = len(image), len(image[0])
    orig_color = image[sr][sc]
    if orig_color == new_color:
        return image

    def _dfs(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols):
            return
        if image[r][c] != orig_color:
            return
        image[r][c] = new_color
        _dfs(r - 1, c)
        _dfs(r + 1, c)
        _dfs(r, c - 1)
        _dfs(r, c + 1)

    _dfs(sr, sc)
    return image


# ---------------------------------------------------------------------------
# Number of Islands
# ---------------------------------------------------------------------------

def num_islands(grid: List[List[str]]) -> int:
    """
    Count the number of islands in a 2D binary grid.

    An island is a group of '1's connected 4-directionally and surrounded by
    water ('0').

    Parameters
    ----------
    grid : List[List[str]]
        Grid of '0's (water) and '1's (land).

    Returns
    -------
    int
        Number of islands.

    Time  : O(rows × cols)
    Space : O(rows × cols) worst-case recursion.
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def _dfs(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols):
            return
        if grid[r][c] != "1":
            return
        grid[r][c] = "#"  # mark visited
        _dfs(r - 1, c)
        _dfs(r + 1, c)
        _dfs(r, c - 1)
        _dfs(r, c + 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                _dfs(r, c)
    return count


# ---------------------------------------------------------------------------
# Surrounded Regions
# ---------------------------------------------------------------------------

def surrounded_regions(board: List[List[str]]) -> None:
    """
    Capture all regions that are 4-directionally surrounded by 'X'.

    A region is captured by flipping all 'O's in that region to 'X', unless
    the region touches the border.

    Parameters
    ----------
    board : List[List[str]]
        Grid of 'X' and 'O'.  Modified in place.

    Time  : O(rows × cols)
    Space : O(rows × cols)

    Example
    -------
    Input:
        X X X X
        X O O X
        X X O X
        X O X X
    Output:
        X X X X
        X X X X
        X X X X
        X O X X    (the bottom-left 'O' touches the border)
    """
    if not board or not board[0]:
        return
    rows, cols = len(board), len(board[0])

    def _dfs(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols):
            return
        if board[r][c] != "O":
            return
        board[r][c] = "S"  # mark as safe
        _dfs(r - 1, c)
        _dfs(r + 1, c)
        _dfs(r, c - 1)
        _dfs(r, c + 1)

    # Mark border-connected 'O's as safe
    for r in range(rows):
        for c in [0, cols - 1]:
            if board[r][c] == "O":
                _dfs(r, c)
    for c in range(cols):
        for r in [0, rows - 1]:
            if board[r][c] == "O":
                _dfs(r, c)

    # Flip remaining 'O' to 'X', safe 'S' back to 'O'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "S":
                board[r][c] = "O"


# ---------------------------------------------------------------------------
# Word Search
# ---------------------------------------------------------------------------

def word_search(board: List[List[str]], word: str) -> bool:
    """
    Determine if `word` exists in a 2D character board.

    The word can be constructed from letters in sequentially adjacent cells,
    where adjacent cells are horizontally or vertically neighbouring.  The
    same cell may not be used more than once.

    Parameters
    ----------
    board : List[List[str]]
        2D character board.
    word : str
        Word to search for.

    Returns
    -------
    bool
        True if the word exists in the board.

    Time  : O(rows × cols × 4^L) where L = len(word).
    Space : O(L) recursion depth.
    """
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])

    def _dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if board[r][c] != word[idx]:
            return False

        # Mark cell as used
        temp = board[r][c]
        board[r][c] = "#"

        found = (_dfs(r - 1, c, idx + 1) or
                 _dfs(r + 1, c, idx + 1) or
                 _dfs(r, c - 1, idx + 1) or
                 _dfs(r, c + 1, idx + 1))

        board[r][c] = temp  # backtrack
        return found

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and _dfs(r, c, 0):
                return True
    return False


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== DFS Tests ===\n")

    # dfs_recursive & dfs_iterative
    g: Dict[int, List[int]] = {
        0: [1, 2], 1: [0, 3], 2: [0, 4],
        3: [1], 4: [2], 5: []
    }
    r1 = dfs_recursive(g, 0)
    r2 = dfs_iterative(g, 0)
    assert r1 == {0, 1, 2, 3, 4}, f"dfs_recursive failed: {r1}"
    assert r2 == {0, 1, 2, 3, 4}, f"dfs_iterative failed: {r2}"
    assert dfs_recursive(g, 5) == {5}
    assert dfs_iterative(g, 5) == {5}
    print("  PASS dfs_recursive & dfs_iterative")

    # flood_fill
    img = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
    result = flood_fill([r[:] for r in img], 1, 1, 2)
    expected = [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    assert result == expected, f"flood_fill: {result} != {expected}"
    print("  PASS flood_fill")

    # num_islands
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands([r[:] for r in grid]) == 3
    assert num_islands([]) == 0
    print("  PASS num_islands")

    # surrounded_regions
    board = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    surrounded_regions(board)
    assert board[3][1] == "O", "Bottom-left should survive"
    assert board[1][1] == "X", "Center should be captured"
    print("  PASS surrounded_regions")

    # word_search
    b = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    assert word_search([r[:] for r in b], "ABCCED") == True
    assert word_search([r[:] for r in b], "SEE") == True
    assert word_search([r[:] for r in b], "ABCB") == False
    print("  PASS word_search")

    print("\nAll DFS tests completed!")
